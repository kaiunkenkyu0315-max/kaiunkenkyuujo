import streamlit as st
from datetime import datetime
import google.generativeai as genai

# APIキーの設定
try:
    # モデル名を 'models/gemini-1.5-flash' とフルネームで指定
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    # 疎通確認（これ自体がエラーになればライブラリかキーの問題）
    response = model.generate_content("test", generation_config={"max_output_tokens": 1})
except Exception as e:
    # 1.5-flashがダメな場合、より安定している1.0-proを試す
    st.warning("Gemini 1.5 Flashの起動に失敗しました。1.0 Proに切り替えます。")
    model = genai.GenerativeModel('gemini-1.0-pro')

st.set_page_config(page_title="行動決定型占い", layout="centered")
st.title("🔮 迷いを行動に変える 占い（AI鑑定版）")

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
                # Gemini API へのプロンプト作成
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

                # APIを呼び出す
                response = model.generate_content(prompt)
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
                st.info("APIのバージョンが古い可能性があります。requirements.txt を更新してください。")

# 履歴表示
st.subheader("過去の占い履歴")
if "history" in st.session_state:
    for entry in reversed(st.session_state.history[-5:]):
        with st.expander(entry["date"]):
            st.markdown(entry["result"])