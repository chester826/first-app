import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from builder import get_best_build

st.set_page_config(page_title="Streamlit PC Builder", page_icon="💻", layout="wide")

# ----------------- 1. 語言包字典 (UI Text) -----------------
TRANSLATIONS = {
    "繁體中文": {
        "title": "💻 Streamlit PC 智慧配單引擎",
        "subtitle": "雙語支援版：預編譯 4×10 矩陣與全組裝清單解析",
        "step1": "🎯 第一步：設定預算與用途需求",
        "budget_label": "最高預算 (USD)",
        "category_label": "主要用途",
        "submit_btn": "🚀 推薦給我最好的組合",
        "warning_no_match": "⚠️ 目前的預算與用途組合找不到符合的配單，請嘗試提高預算！",
        "recommend_title": "💡 系統推薦最佳組合：${budget} USD ({category}導向)",
        "specs_header": "### 🛠️ 預先編譯優化組裝清單",
        "col_component": "組件類別",
        "col_model": "選用型號與規格",
        "parts": ["處理器 (CPU)", "顯示卡 (GPU)", "主機板 (MB)", "記憶體 (RAM)", "儲存 (SSD)", "電源 (PSU)", "機殼 (Case)"],
        "radar_header": "### 📊 效能三維雷達圖",
        "radar_labels": ['遊戲效能', '生產力', 'AI 運算', '遊戲效能'],
        "info_prompt": "👈 請設定預算與用途後，點擊「推薦給我最好的組合」按鈕查看預先編譯的完整組裝菜單。"
    },
    "English": {
        "title": "💻 Streamlit PC Builder Engine",
        "subtitle": "Bilingual Edition: Pre-compiled 4×10 Matrix & Full Specs Analysis",
        "step1": "🎯 Step 1: Set Your Budget & Usage",
        "budget_label": "Max Budget (USD)",
        "category_label": "Primary Usage",
        "submit_btn": "🚀 Recommend the Best Build",
        "warning_no_match": "⚠️ No compatible build found for this budget and usage. Please increase your budget!",
        "recommend_title": "💡 Recommended Build: ${budget} USD ({category} Focused)",
        "specs_header": "### 🛠️ Pre-compiled Optimized Part List",
        "col_component": "Component",
        "col_model": "Selected Model & Specs",
        "parts": ["Processor (CPU)", "Graphics Card (GPU)", "Motherboard (MB)", "Memory (RAM)", "Storage (SSD)", "Power Supply (PSU)", "Case"],
        "radar_header": "### 📊 3D Performance Radar",
        "radar_labels": ['Gaming', 'Productivity', 'AI Compute', 'Gaming'],
        "info_prompt": "👈 Set your budget and usage above, then click 'Recommend the Best Build' to view your complete part list."
    }
}

# ----------------- 2. 資料層轉譯橋樑 (Data Mapping) -----------------
# 負責將前端顯示的選項，對應回 database.csv 裡面的中文欄位值
CATEGORY_MAP = {
    "繁體中文": {"文書": "文書", "遊戲": "遊戲", "創作": "創作", "生產力": "生產力", "AI": "AI"},
    "English": {"Office": "文書", "Gaming": "遊戲", "Creator": "創作", "Productivity": "生產力", "AI": "AI"}
}

# ----------------- 語言切換器 (放置在右上角或側邊欄) -----------------
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    lang = st.selectbox("🌐 Language / 語言", options=["English", "繁體中文"], index=0)

# 取得當前語言的字典包
t = TRANSLATIONS[lang]

with top_col1:
    st.title(t["title"])
    st.write(t["subtitle"])

#@st.cache_data
def load_data():
    return pd.read_csv("database.csv")

df = load_data()

# --- UI 輸入區 ---
st.subheader(t["step1"])
col1, col2 = st.columns(2)

with col1:
    user_budget = st.slider(
        t["budget_label"], 
        min_value=int(df['Budget'].min()), 
        max_value=int(df['Budget'].max()), 
        value=2000, 
        step=100
    )

with col2:
    # 動態抓取資料庫中實際存在的類別，並轉換為當前語言的選項
    available_cn_categories = df['Category'].unique()
    display_categories = [
        k for k, v in CATEGORY_MAP[lang].items() if v in available_cn_categories
    ]
    selected_display_cat = st.selectbox(t["category_label"], options=display_categories)
    
    # 將使用者選的語言（例如 "Gaming"）轉譯回 CSV 看得懂的中文（"遊戲"）
    actual_category_for_db = CATEGORY_MAP[lang][selected_display_cat]

st.divider()

submit_button = st.button(t["submit_btn"], type="primary", use_container_width=True)

# --- 演算與展示區 ---
if submit_button:
    # 傳給 builder.py 的依然是轉譯後的中文類別，確保布林遮罩不會失效
    best_match = get_best_build(df, user_budget, actual_category_for_db)

    if best_match is None:
        st.warning(t["warning_no_match"])
    else:
        st.subheader(t["recommend_title"].format(budget=best_match['Budget'], category=selected_display_cat))
        
        res_col1, res_col2 = st.columns([3, 2])

        with res_col1:
            st.markdown(t["specs_header"])
            
            # 處理硬體規格裡的中文詞彙（例如將「內顯」自動替換為英文 IGP）
            gpu_val = best_match['GPU']
            if lang == "English" and "內顯" in str(gpu_val):
                gpu_val = str(gpu_val).replace("內顯", "Integrated Graphics")

            specs_df = pd.DataFrame({
                t["col_component"]: t["parts"],
                t["col_model"]: [
                    best_match['CPU'], 
                    gpu_val, 
                    best_match['Motherboard'], 
                    best_match['RAM'], 
                    best_match['Storage'], 
                    best_match['PSU'], 
                    best_match['Case']
                ]
            })
            st.table(specs_df)

        with res_col2:
            st.markdown(t["radar_header"])
            categories_radar = t["radar_labels"]
            scores = [best_match['Score_Gaming'], best_match['Score_Work'], best_match['Score_AI'], best_match['Score_Gaming']]

            fig = go.Figure(go.Scatterpolar(
                r=scores, theta=categories_radar, fill='toself', line_color='#00b4d8'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info(t["info_prompt"])