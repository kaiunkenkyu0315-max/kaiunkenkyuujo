import streamlit as st
import google.generativeai as genai

# あなたの最新のAPIキーに書き換えてください
genai.configure(api_key="最新のAPIキーをここに貼る")

st.title("Gemini 接続テスト")

# あえてモデル名から 'models/' を外した最も標準的な書き方
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, how are you?")
    st.success("成功！Gemini 1.5 Flash は正常に動いています。")
    st.write(response.text)
except Exception as e:
    st.error(f"エラーが発生しました: {e}")
    st.info("このエラーが出る場合、サーバー側のライブラリ更新が反映されていません。")