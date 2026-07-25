import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 從獨立的 builder.py 檔案引入我們的配單演算法
from builder import get_best_build

st.set_page_config(page_title="Streamlit PC Builder", page_icon="💻", layout="wide")

st.title("💻 Streamlit PC Builder")
st.write("第 9 步進階：導入「推薦按鈕」延遲計算機制")

@st.cache_data
def load_data():
    return pd.read_csv("database.csv")

df = load_data()

# --- 前端 UI 輸入區 ---
st.subheader("🎯 第一步：請設定您的預算與需求")
col1, col2 = st.columns(2)

with col1:
    user_budget = st.slider("設定您的預算 (USD)", min_value=int(df['Budget'].min()), max_value=int(df['Budget'].max()), value=2000, step=100)

with col2:
    user_category = st.selectbox("主要用途", options=df['Category'].unique())

st.divider()

# --- 核心改動：觸發按鈕 ---
# 使用 use_container_width=True 讓按鈕橫跨整欄，更醒目
submit_button = st.button("🚀 推薦給我最好的組合", type="primary", use_container_width=True)

# --- 前端渲染與演算區 ---
# 只有當 submit_button 為 True (被按下) 時，才執行裡面的運算與渲染
if submit_button:
    # 呼叫 builder.py 大腦
    best_match = get_best_build(df, user_budget, user_category)

    if best_match is None:
        st.warning("⚠️ 目前的預算找不到符合的配置，請提高預算！")
    else:
        st.subheader("💡 系統為您生成的最佳推薦配置")
        res_col1, res_col2 = st.columns(2)

        with res_col1:
            st.success(f"✅ 成功找到推薦配置：{best_match['Category']}")
            st.write(f"**CPU:** {best_match['CPU']}")
            st.write(f"**GPU:** {best_match['GPU']}")
            st.write(f"**RAM:** {best_match['RAM']}")
            st.write(f"**Storage:** {best_match['Storage']}")
            st.info(f"💰 總價格: **${best_match['Budget']} USD**")

        with res_col2:
            categories_radar = ['遊戲效能', '生產力', 'AI 運算', '遊戲效能'] 
            scores = [best_match['Score_Gaming'], best_match['Score_Work'], best_match['Score_AI'], best_match['Score_Gaming']]

            fig = go.Figure(go.Scatterpolar(
                r=scores, theta=categories_radar, fill='toself', line_color='#00b4d8'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
else:
    # 當按鈕還沒被按下時，顯示引導提示
    st.info("👈 請在上方設定預算與用途後，點擊「推薦給我最好的組合」按鈕開始配單。")