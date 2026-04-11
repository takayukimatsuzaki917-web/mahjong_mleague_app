import streamlit as st  # 画面を作るライブラリ

from calculator import MahjongScoreCalculator, MLeaguePointCalculator
from models import HandInput, MLeagueScoreInput, WinnerType, WinType


# ページ設定
st.set_page_config(page_title="麻雀アプリ", layout="wide")

# タイトル
st.title("麻雀点数計算アプリ")

# タブ作成（画面切り替え）
tab1, tab2 = st.tabs(["和了点", "Mリーグ"])


# ===== 和了点計算 =====
with tab1:

    st.subheader("和了点計算")

    # フォーム（まとめて入力）
    with st.form("form"):

        # 横に並べる
        col1, col2 = st.columns(2)

        with col1:
            fu = st.selectbox("符", [20, 30, 40, 50])
            han = st.selectbox("翻", [1, 2, 3, 4, 5])

        with col2:
            winner_type = st.radio("親/子", ["親", "子"])
            win_type = st.radio("ロン/ツモ", ["ロン", "ツモ"])

        # ボタン
        submitted = st.form_submit_button("計算")

    # ボタン押したら実行
    if submitted:

        # 入力データ作成
        hand_input = HandInput(
            fu=fu,
            han=han,
            winner_type=WinnerType(winner_type),
            win_type=WinType(win_type),
        )

        # 計算
        result = MahjongScoreCalculator.calculate_hand_score(hand_input)

        # 表示
        st.metric("基本点", result.base_points)
        st.metric("結果", result.total_points)


# ===== Mリーグ =====
with tab2:

    st.subheader("最終ポイント")

    with st.form("score_form"):

        # 4人入力
        p1 = st.number_input("P1", value=25000)
        p2 = st.number_input("P2", value=25000)
        p3 = st.number_input("P3", value=25000)
        p4 = st.number_input("P4", value=25000)

        submitted = st.form_submit_button("計算")

    if submitted:

        scores = [p1, p2, p3, p4]

        result = MLeaguePointCalculator.calculate(
            MLeagueScoreInput(scores=scores)
        )

        # 表示
        for i, p in enumerate(result.players):
            st.write(f"P{i+1}: 順位 {p.rank} / {p.point}pt")