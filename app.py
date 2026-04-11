import streamlit as st

from calculator import MahjongScoreCalculator, MLeaguePointCalculator
from models import HandInput, MLeagueScoreInput, WinnerType, WinType


st.set_page_config(page_title="Mリーグ麻雀点数計算アプリ", layout="wide")

st.title("Mリーグ麻雀点数計算アプリ")
st.caption("役の翻数を入力すると、場ゾロ2翻を自動加算してMリーグ寄りに計算します。")

tab1, tab2 = st.tabs(["和了点計算", "Mリーグ最終ポイント計算"])


with tab1:
    st.subheader("和了点計算")

    with st.form("hand_score_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            fu = st.selectbox("符", [20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110], index=2)
            han = st.selectbox("役の翻数（場ゾロ抜き）", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=1)

        with col2:
            winner_type = st.radio("親 / 子", [WinnerType.DEALER.value, WinnerType.NON_DEALER.value])
            win_type = st.radio("ロン / ツモ", [WinType.RON.value, WinType.TSUMO.value])

        with col3:
            honba = st.number_input("本場", min_value=0, max_value=20, value=0, step=1)
            kyotaku = st.number_input("供託（本数）", min_value=0, max_value=20, value=0, step=1)

        submitted = st.form_submit_button("計算する")

    if submitted:
        try:
            hand_input = HandInput(
                fu=fu,
                han=han,
                winner_type=WinnerType(winner_type),
                win_type=WinType(win_type),
                honba=honba,
                kyotaku=kyotaku,
                include_bazoro=True,
            )
            result = MahjongScoreCalculator.calculate_hand_score(hand_input)

            st.success("計算完了")
            st.metric("基本点", f"{result.base_points}")
            st.metric("和了点", result.total_points)
            st.info(f"今回の計算では、役の翻数 {han}翻 に場ゾロ2翻を加えて計算しています。")

        except Exception as e:
            st.error(f"エラー: {e}")