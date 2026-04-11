import math

from models import (
    HandInput,
    HandResult,
    MLeagueScoreInput,
    MLeagueScoreResult,
    PlayerMLeagueResult,
    WinnerType,
    WinType,
)


class MahjongScoreCalculator:
    """Mリーグ寄りの和了点計算クラス"""

    @staticmethod
    def _round_up_to_100(value: int) -> int:
        # 100点単位に切り上げる
        return int(math.ceil(value / 100.0) * 100)

    @staticmethod
    def _effective_han(hand: HandInput) -> int:
        """
        実際の計算に使う翻数を返す。
        Mリーグでは場ゾロ2翻を含めて計算するため、
        include_bazoro=True のときは +2 する。
        """
        han = hand.han
        if hand.include_bazoro:
            han += 2
        return han

    @staticmethod
    def _calc_base_points(fu: int, han: int) -> int:
        """
        基本点を計算する。
        han は「場ゾロ込み」の翻数で受け取る。
        """
        if han <= 0:
            raise ValueError("翻数は1以上で入力してください。")
        if fu <= 0:
            raise ValueError("符は1以上で入力してください。")

        # 満貫以上の判定
        # Mリーグ公式では、
        # ・20符以上の7翻
        # ・30符以上の6翻と7翻
        # ・60符以上の5翻
        # を満貫とする
        if han >= 13:
            return 8000  # 役満
        if han >= 11:
            return 6000  # 三倍満
        if han >= 8:
            return 4000  # 倍満
        if han >= 6:
            return 3000  # 跳満

        # 5翻は満貫
        if han == 5:
            return 2000

        # 30符6翻は切り上げ満貫、という考え方は
        # 上の han >= 6 に含まれる。
        # 4翻以下は通常計算
        # ただし一般的な満貫ラインも残しておく
        if han == 4 and fu >= 40:
            return 2000
        if han == 3 and fu >= 70:
            return 2000

        return fu * (2 ** (han + 2))

    @classmethod
    def calculate_hand_score(cls, hand: HandInput) -> HandResult:
        # 場ゾロ込み翻数を計算
        effective_han = cls._effective_han(hand)

        # 基本点を計算
        base_points = cls._calc_base_points(hand.fu, effective_han)

        # ロン和了
        if hand.win_type == WinType.RON:
            if hand.winner_type == WinnerType.DEALER:
                ron_points = cls._round_up_to_100(base_points * 6)
            else:
                ron_points = cls._round_up_to_100(base_points * 4)

            ron_points += hand.honba * 300
            ron_points += hand.kyotaku * 1000

            return HandResult(
                base_points=base_points,
                total_points=f"{ron_points}点",
                rounded_points=ron_points,
            )

        # ツモ和了
        if hand.winner_type == WinnerType.DEALER:
            payment_each = cls._round_up_to_100(base_points * 2)
            total = payment_each * 3 + hand.honba * 300 + hand.kyotaku * 1000

            return HandResult(
                base_points=base_points,
                total_points=f"{payment_each}点オール（合計 {total}点）",
                dealer_payment=payment_each,
            )

        # 子ツモ
        non_dealer_payment = cls._round_up_to_100(base_points * 1)
        dealer_payment = cls._round_up_to_100(base_points * 2)
        total = dealer_payment + non_dealer_payment * 2 + hand.honba * 300 + hand.kyotaku * 1000

        return HandResult(
            base_points=base_points,
            total_points=f"親 {dealer_payment}点 / 子 {non_dealer_payment}点（合計 {total}点）",
            dealer_payment=dealer_payment,
            non_dealer_payment=non_dealer_payment,
        )


class MLeaguePointCalculator:
    RANK_POINTS = {
        1: 50.0,
        2: 10.0,
        3: -10.0,
        4: -30.0,
    }

    @classmethod
    def calculate(cls, score_input: MLeagueScoreInput) -> MLeagueScoreResult:
        if len(score_input.scores) != 4:
            raise ValueError("4人分の素点を入力してください。")

        indexed_scores = list(enumerate(score_input.scores))
        indexed_scores.sort(key=lambda x: x[1], reverse=True)

        players_result = [None] * 4
        current_rank = 1

        for sorted_index, (player_index, score) in enumerate(indexed_scores):
            if sorted_index > 0 and score < indexed_scores[sorted_index - 1][1]:
                current_rank = sorted_index + 1

            point = (score - 30000) / 1000 + cls.RANK_POINTS[current_rank]

            players_result[player_index] = PlayerMLeagueResult(
                rank=current_rank,
                score=score,
                point=round(point, 1),
            )

        return MLeagueScoreResult(players=players_result)