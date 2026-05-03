import streamlit as st
from datetime import datetime
import google.generativeai as genai

st.set_page_config(page_title="行動決定型占い", layout="centered")
st.title("🔮 迷いを行動に変える 無料占い")

# === Gemini API設定（ここにあなたのAPIキーを入れる）===
genai.configure(api_key="AIzaSyDfABeDgcXy7-qID_2TMJFB24FeD0QSmSQ")  # ← ここを自分のキーに変更

model = genai.GenerativeModel('gemini-1.5-flash')

# ユーザーID
if "user_id" not in st.session_state:
    user_id = st.text_input("ニックネーム or アカウント名（履歴用）", placeholder="例: taro_test")
    if st.button("スタート"):
        if user_id:
            st.session_state.user_id = user_id
            st.rerun()
    st.stop()

st.sidebar.success(f"ログイン中: {st.session_state.user_id}")

# 入力
st.subheader("あなたの状況を教えてください")
issue = st.text_area("1. 今、決断できずに止まっていること", height=100)
situation = st.text_area("2. 現在の状況（短く）", height=80)

if st.button("占う", type="primary"):
    if not issue or not situation:
        st.error("両方入力してください")
    else:
        with st.spinner("AI占い師が鑑定中..."):
            prompt = f"""
# Role: 迷いを「行動」に変える専門家
あなたは論理的かつ直感的な行動決定型占い師です。

ユーザーの情報:
- 決断できずに止まっていること: {issue}
- 現在の状況: {situation}

以下の3点のみで出力してください：
1. 【今の状態】：鋭い洞察で言語化
2. 【1つの警告】：具体的リスクを1つ
3. 【1つの行動】：今すぐできる小さなアクション

最後に以下の誘導文を必ず付けて：
---
※今のあなたには「さらに深い深層心理のバグ」と「3ヶ月先の詳細ロードマップ」が必要です。
これらを網羅した【完全版占い】は、noteにて詳細に解説しています。
[あなたのnoteリンク]
"""

            response = model.generate_content(prompt)
            result_text = response.text

            st.success("占い完了")
            st.markdown(result_text)

            # 履歴保存
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "issue": issue,
                "result": result_text
            })

# 履歴表示（簡易）
st.subheader("📜 過去の占い履歴")
if "history" in st.session_state and st.session_state.history:
    for entry in reversed(st.session_state.history[-5:]):  # 最新5件
        with st.expander(f"{entry['date']} - {entry['issue'][:30]}..."):
            st.markdown(entry['result'])
else:
    st.info("履歴はここに表示されます")