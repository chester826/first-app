import streamlit as st
import pandas as pd

st.set_page_config(page_title="PromptPC 語意配單引擎", page_icon="🧠")

st.title("🧠 PromptPC 語意配單引擎")
st.write("核心測試：動態條件篩選")

@st.cache_data
def load_data():
    return pd.read_csv("database.csv")

df = load_data()

# ----------------- UI 互動區 -----------------
st.subheader("🎯 步驟一：設定您的需求")

# 使用 columns 讓畫面排版更緊湊 (切成左右兩排)
col1, col2 = st.columns(2)

with col1:
    # 前瞻性寫法：讓滑桿的最小值與最大值，自動跟著資料庫變動，而不是寫死
    min_budget = int(df['Budget'].min())
    max_budget = int(df['Budget'].max())
    user_budget = st.slider("最高預算 (USD)", min_value=min_budget, max_value=max_budget, value=2000, step=100)

with col2:
    # 前瞻性寫法：動態抓取資料庫裡所有不重複的「用途 (Category)」
    categories = df['Category'].unique()
    user_category = st.selectbox("主要用途", options=categories)

st.divider() # 畫一條視覺分隔線

# ----------------- 演算法與邏輯區 -----------------
st.subheader("💡 系統推薦配單")

# Pandas 矩陣過濾邏輯 (Masking)
# 條件一：配單預算 <= 使用者設定的預算
# 條件二：配單用途 == 使用者選擇的用途
mask = (df['Budget'] <= user_budget) & (df['Category'] == user_category)
filtered_df = df[mask]

# ----------------- 渲染結果區 -----------------
if filtered_df.empty:
    # 如果過濾後沒有資料 (例如預算太低)
    st.warning("⚠️ 目前的預算與用途組合，找不到符合的配單。請嘗試提高預算！")
else:
    st.success(f"✅ 成功為您找到 {len(filtered_df)} 筆最佳配置！")
    st.dataframe(filtered_df)