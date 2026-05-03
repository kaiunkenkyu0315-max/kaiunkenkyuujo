import streamlit as st
from datetime import datetime
import google.generativeai as genai

genai.configure(api_key="AIzaSyBadkCUK12PZ4h6ChGfCtmn0XWSmwF7F2I")
model = genai.GenerativeModel('gemini-1.5-flash') # モデル名を直接指定

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
        # 簡易AI風占い（入力に基づいて変化）
        state_templates = [
            f"あなたは「{issue}」に対して完璧を求めすぎて行動をブロックしています。",
            f"現在の状況（{situation}）の中で、心の奥底で恐れを抱いている部分があります。"
        ]
        warning_templates = [
            "このままでは機会を失い、後悔が残ります。",
            "周囲の人が先に動いてしまい、置いていかれる可能性があります。"
        ]
        action_templates = [
            "今日中にそのことについて1行だけメモを書く。",
            "5分だけ関連する情報を検索してみる。"
        ]

        result = f"""
### 鑑定結果

**【今の状態】**  
{random.choice(state_templates)}

**【1つの警告】**  
{random.choice(warning_templates)}

**【1つの行動】**  
{random.choice(action_templates)}
"""

        st.markdown(result)
        st.markdown("---")
        st.markdown("※さらに深い分析はnote完全版で → [noteリンク]")
        
        # 履歴保存
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "result": result})

# 履歴
st.subheader("過去の占い履歴")
if "history" in st.session_state:
    for entry in reversed(st.session_state.history[-5:]):
        with st.expander(entry["date"]):
            st.markdown(entry["result"])