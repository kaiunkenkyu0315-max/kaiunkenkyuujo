import streamlit as st
from datetime import datetime
from google import genai  # 新しいSDK

# APIキーの設定
# ※ GitHub公開時は Streamlit の Secrets 設定を推奨します
client = genai.Client(api_key="AIzaSyBadkCUK12PZ4h6ChGfCtmn0XWSmwF7F2I")

st.set_page_config(page_title="行動決定型占い", layout="centered")
st.title("🔮 迷いを行動に変える 無料占い")

if "user_id" not in st.session_state:
    user_id = st.text_input("ニックネーム or メール（履歴用）", placeholder="例: taro_test")
    if st.button("スタート"):
        if user_id:
            st.session_state.user_id = user_id
            st.rerun()
    st.stop()

st.sidebar.success(f"ログイン中: {st.session_state.user_id}")

st.subheader("あなたの状況を教えてください")
issue = st.text_area("1. 今、決断できずに止まっていること", height=100)
situation = st.text_area("2. 現在の状況（短く）", height=80)

if st.button("占う", type="primary"):
    if not issue or not situation:
        st.error("両方入力してください")
    else:
        with st.spinner("AIが鑑定中..."):
            try:
                # 最新のSDK（google-genai）での呼び出し方法
                prompt = f"""
                あなたは凄腕の占い師です。以下の悩みを持つユーザーに対して、
                「今の状態」「1つの警告」「1つの具体的な行動」の3点を鑑定してください。

                【悩み】: {issue}
                【状況】: {situation}

                形式:
                ### 鑑定結果
                **【今の状態】**
                (ここに鑑定結果)
                **【1つの警告】**
                (ここに厳しい警告)
                **【1つの行動】**
                (今日からできる具体的な一歩)
                """

                # モデルには最新の gemini-2.0-flash を指定
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                result = response.text

                st.markdown(result)
                st.markdown("---")
                st.markdown("※さらに深い分析はnote完全版で → [noteリンク]")
                
                # 履歴保存
                if "history" not in st.session_state:
                    st.session_state.history = []
                st.session_state.history.append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
                    "result": result
                })

            except Exception as e:
                st.error(f"占い中にエラーが発生しました: {e}")

# 履歴表示
st.subheader("過去の占い履歴")
if "history" in st.session_state:
    for entry in reversed(st.session_state.history[-5:]):
        with st.expander(entry["date"]):
            st.markdown(entry["result"])