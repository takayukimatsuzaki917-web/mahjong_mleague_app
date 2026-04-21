import streamlit as st

from calculator import MarkovChainCalculator
from models import HandInput, YakuMaster

st.set_page_config(page_title="麻雀点数計算アプリ", page_icon="🀄", layout="wide")

calculator = MarkovChainCalculator()

def get_fu_options(selected_yaku: List[str]) -> List[int]:
    
    #選択された役に応じて符の選択肢を提供する関数
    #七対子が選択されている場合は符は25固定、それ以外の場合は一般的な符の選択肢を提供
    
    if "七対子" in selected_yaku:
        return [25]
    else:
        return [20, 25, 30, 40, 50, 60, 70, 80, 90, 100]

def main() -> None:
    
    st.title("🀄 麻雀点数計算アプリ")
    st.caption("役を選択すると翻数を自動計算します。七対子選択時は25符固定です。")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("入力")
        
        is_menzen = st.radio(
            "門前 or 副露",
            options = [True, False],
            format_func = lambda x: "門前" if x else "副露"
            horizontal = True,
        )
        
        is_tsumo = st.radio(
            "ツモ or ロン",
            options = [True, False],
            format_func = lambda x: "ツモ" if x else "ロン",
            horizontal = True,
        )   
        
        is_oya = st.radio(
            "親 or 子",
            options = [True, False],
            format_func = lambda x: "親" if x else "子",
            horizontal = True,
        )
        
        st.markdown("### 役の選択")
        yaku_names = list(YakuMaster.keys())
        selected_yaku = st.multiselect(
            "役を選択してください", options=yaku_names,
            default = [],
        )
        
        st.markdown("### 符の選択")
        fu_options = get_fu_options(selected_yaku)
        
        if "七対子" in selected_yaku:
            st.info("七対子が選択されているため、符は25固定です。")
            
        fu = st.selectbox(
            "符を選択してください",
            options=fu_options, 
            index=0        
        )   
        
        st.markdown("### ドラ")
        dora_count = st.number_input("ドラ枚数", min_value=0, max_value=20, value=0, step=1)
        uradora_count = st.number_input("裏ドラ枚数", min_value=0, max_value=20, value=0, step=1)
        akadora_count = st.number_input("赤ドラ枚数", min_value=0, max_value=20, value=0, step=1)

        st.markdown("### 場況")
        honba = st.number_input("本場", min_value=0, max_value=20, value=0, step=1)
        riichi_sticks = st.number_input("供託リーチ棒", min_value=0, max_value=20, value=0, step=1)

    hand = HandInput(
        selected_yaku=selected_yaku,
        is_menzen=is_menzen,
        is_tsumo=is_tsumo,
        is_oya=is_oya,
        fu=fu,
        honba=honba,
        riichi_sticks=riichi_sticks,
        dora_count=dora_count,
        uradora_count=uradora_count,
        akadora_count=akadora_count,
    )

    errors = calculator.validate_hand(hand)

    with col2:
        st.subheader("計算結果")

        if errors:
            for error in errors:
                st.error(error)
            return

        han_breakdown = calculator.calculate_han_breakdown(hand)
        total_han = calculator.calculate_total_han(hand)
        score_result = calculator.calculate_score(hand)
        score_title = calculator.get_score_title(
            han=score_result["han"],
            base_points=score_result["base_points"],
        )

        st.metric("合計翻数", f"{total_han}翻")
        st.metric("符", f"{hand.fu}符")
        st.metric("打点区分", score_title)

        st.markdown("### 翻数内訳")
        if han_breakdown:
            for name, han in han_breakdown.items():
                st.write(f"- {name}: {han}翻")
        else:
            st.write("翻数なし")

        st.markdown("### 点数")
        st.write(f"基本点: {score_result['base_points']}")

        if hand.is_tsumo:
            st.success(f"{score_result['label']}")
            st.write(f"総獲得点（本場・供託込み）: {score_result['total_points']}点")
        else:
            st.success(f"{score_result['label']} {score_result['ron_points']}点")
            st.write(f"総獲得点（本場・供託込み）: {score_result['total_points']}点")

        st.markdown("---")
        st.markdown("### 入力内容確認")
        st.write(f"- 門前: {'はい' if hand.is_menzen else 'いいえ'}")
        st.write(f"- 和了方法: {'ツモ' if hand.is_tsumo else 'ロン'}")
        st.write(f"- 親: {'親' if hand.is_oya else '子'}")
        st.write(f"- 選択役: {', '.join(hand.selected_yaku) if hand.selected_yaku else 'なし'}")
        st.write(f"- ドラ: {hand.dora_count}")
        st.write(f"- 裏ドラ: {hand.uradora_count}")
        st.write(f"- 赤ドラ: {hand.akadora_count}")
        st.write(f"- 本場: {hand.honba}")
        st.write(f"- 供託リーチ棒: {hand.riichi_sticks}")


if __name__ == "__main__":
    main()