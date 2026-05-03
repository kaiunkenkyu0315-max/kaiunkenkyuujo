import streamlit as st
from datetime import datetime
import google.generativeai as genai

st.set_page_config(page_title="行動決定型占い", layout="centered")
st.title("🔮 迷いを行動に変える 無料占い")

# ================== Gemini設定 ==================
genai.configure(api_key="AIzaSyBadkCUK12PZ4h6ChGfCtmn0XWSmwF7F2I")

model = genai.GenerativeModel('gemini-1.5-flash')
# ===============================================

# ユーザーID部分（省略せず前回のコードを残す）
if "user_id" not in st.session_state:
    user_id = st.text_input("ニックネーム or メール（履歴用）", placeholder="例: taro_test")
    if st.button("スタート"):
        if user_id:
            st.session_state.user_id = user_id
            st.rerun()
    st.stop()

# 以下は前回の入力フォーム + prompt部分は変更せず
st.sidebar.success(f"ログイン中: {st.session_state.user_id}")

st.subheader("あなたの状況を教えてください")
issue = st.text_area("1. 今、決断できずに止まっていること", height=100)
situation = st.text_area("2. 現在の状況（短く）", height=80)

if st.button("占う", type="primary"):
    if not issue or not situation:
        st.error("両方入力してください")
    else:
        with st.spinner("AI占い師が鑑定中..."):
            prompt = f"""...（前回のprompt全文）..."""   # 前回のpromptをここに貼る

            response = model.generate_content(prompt)
            st.markdown(response.text)