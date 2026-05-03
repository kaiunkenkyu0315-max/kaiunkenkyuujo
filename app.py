import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="行動決定型占い", layout="centered")
st.title("🔮 迷いを行動に変える 無料占い")

# ユーザー識別（簡易）
if "user_id" not in st.session_state:
    user_id = st.text_input("ニックネーム or メールアドレス（履歴保存用）", placeholder="例: taro_uranai")
    if st.button("スタート"):
        if user_id:
            st.session_state.user_id = user_id
            st.rerun()
        else:
            st.warning("ニックネームを入力してください")
    st.stop()

st.sidebar.success(f"ログイン中: {st.session_state.user_id}")

# ヒアリング
st.subheader("あなたの状況を教えてください")
issue = st.text_area("1. 今、決断できずに止まっていること", height=100)
situation = st.text_area("2. 現在の状況（短く）", height=80)

if st.button("占う", type="primary"):
    if not issue or not situation:
        st.error("両方入力してください")
    else:
        with st.spinner("占い中..."):
            # ここに本格的なLLM呼び出しを入れる（現在は簡易版）
            result = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "issue": issue,
                "state": "【今の状態】\nあなたは頭では理解していながらも、心のどこかで完璧を求めすぎて行動を先送りにしている状態です。表面的な「忙しさ」に隠れて、本当の優先順位が見えにくくなっています。",
                "warning": "【1つの警告】\nこのまま3ヶ月放置すると、せっかくの機会が他者に取られ、結果として『あの時動いていれば...』という強い後悔と機会損失が生じます。",
                "action": "【1つの行動】\n今日中に、たった5分でいいので「決断できずに止まっていること」に関連する資料やメモを1ページだけ開いてみる。完璧じゃなくていい、ただ「触れる」だけでOKです。"
            }
            
            # 表示
            st.success("占い完了")
            st.markdown("### 鑑定結果")
            st.markdown(result["state"])
            st.markdown(result["warning"])
            st.markdown(result["action"])
            
            # 誘導文
            st.markdown("---")
            st.markdown("""
            ※今のあなたには「さらに深い深層心理のバグ」と「3ヶ月先の詳細ロードマップ」が必要です。  
            これらを網羅した【完全版占い】は、noteにて詳細に解説しています。  
            → [noteリンクをここに貼ってください]
            """)
            
            # 履歴に保存
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(result)
            
            st.balloons()

# 履歴表示
st.subheader("📜 過去の占い履歴")
if "history" in st.session_state and st.session_state.history:
    for i, entry in enumerate(reversed(st.session_state.history)):
        with st.expander(f"{entry['date']} - {entry['issue'][:30]}..."):
            st.markdown(entry["state"])
            st.markdown(entry["warning"])
            st.markdown(entry["action"])
else:
    st.info("まだ占い履歴がありません。初めて占ってみましょう！")

# サイドバー情報
st.sidebar.info("この占いは「行動」を重視したものです。\n完全版はnoteでご覧ください。")