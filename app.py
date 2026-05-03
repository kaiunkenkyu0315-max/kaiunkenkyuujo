import streamlit as st
from google import genai  # 新しいインポート方法

# APIキーの設定（最新版の書き方）
client = genai.Client(api_key="AIzaSyBadkCUK12PZ4h6ChGfCtmn0XWSmwF7F2I")

st.title("🔮 占い（最新版SDK）")

# （中略：ユーザー入力部分などはそのまま）

if st.button("占う"):
    try:
        # 最新の呼び出しメソッド
        response = client.models.generate_content(
            model="gemini-2.0-flash", # 最新モデルも使えます
            contents=f"悩み: {issue}, 状況: {situation} を占って"
        )
        st.markdown(response.text)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")