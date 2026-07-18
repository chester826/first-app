import streamlit as st

# 設定網頁標題
st.set_page_config(page_title="PromptPC 語意配單引擎", page_icon="🧠")

st.title("🧠 PromptPC 語意配單引擎")
st.write("用最直白的語言，打造最懂你的硬體。")

# 預算輸入
budget = st.slider("請設定您的最高預算 (USD)", min_value=500, max_value=10000, value=2000, step=100)

# 提交按鈕
if st.button("🚀 開始組裝"):
    st.success(f"系統已收到指示！將為您尋找 {budget} 美金以下的最佳配置...")