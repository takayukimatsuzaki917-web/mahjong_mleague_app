import math  # 切り上げ計算などに使う

# 型（データの形）をmodelsから読み込む
from models import (
    HandInput,
    HandResult,
    MLeagueScoreInput,
    MLeagueScoreResult,
    PlayerMLeagueResult,
    WinnerType,
    WinType,
)


# 麻雀の点数計算クラス
class MahjongScoreCalculator:

    # 100点単位に切り上げる関数
    @staticmethod
    def _round_up_to_100(value: int) -> int:
        return int(math.ceil(value / 100.0) * 100)

    # 基本点を計算する関数
    @staticmethod
    def _calc_base_points(fu: int, han: int) -> int:

        # 入力チェック
        if han <= 0:
            raise ValueError("翻数は1以上")
        if fu <= 0:
            raise ValueError("符は1以上")

        # 満貫以上の処理
        if han >= 13:
            return 8000  # 役満
        if han >= 11:
            return 6000  # 三倍満
        if han >= 8:
            return 4000  # 倍満
        if han >= 6:
            return 3000  # 跳満
        if han == 5:
            return 2000  # 満貫

        # 特殊満貫
        if han == 4 and fu >= 40:
            return 2000
        if han == 3 and fu >= 70:
            return 2000

        # 通常計算
        return fu * (2 ** (han + 2))

    # 実際の点数計算
    @classmethod
    def calculate_hand_score(cls, hand: HandInput) -> HandResult:

        # 基本点を計算
        base_points = cls._calc_base_points(hand.fu, hand.han)

        # ロンの場合
        if hand.win_type == WinType.RON:

            if hand.winner_type == WinnerType.DEALER:
                ron_points = cls._round_up_to_100(base_points * 6)
            else:
                ron_points = cls._round_up_to_100(base_points * 4)

            # 本場と供託を加算
            ron_points += hand.honba * 300
            ron_points += hand.kyotaku * 1000

            return HandResult(
                base_points=base_points,
                total_points=f"{ron_points}点",
                rounded_points=ron_points,
            )

        # ツモの場合
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


# Mリーグのポイント計算
class MLeaguePointCalculator:

    # 順位点
    RANK_POINTS = {
        1: 50.0,
        2: 10.0,
        3: -10.0,
        4: -30.0,
    }

    @classmethod
    def calculate(cls, score_input: MLeagueScoreInput) -> MLeagueScoreResult:

        # 4人チェック
        if len(score_input.scores) != 4:
            raise ValueError("4人分必要")

        # プレイヤー番号と点数をセットにする
        indexed_scores = list(enumerate(score_input.scores))

        # 点数で並び替え（高い順）
        indexed_scores.sort(key=lambda x: x[1], reverse=True)

        players_result = [None] * 4

        current_rank = 1

        for sorted_index, (player_index, score) in enumerate(indexed_scores):

            # 同点でない場合は順位更新
            if sorted_index > 0 and score < indexed_scores[sorted_index - 1][1]:
                current_rank = sorted_index + 1

            # ポイント計算
            point = (score - 30000) / 1000 + cls.RANK_POINTS[current_rank]

            players_result[player_index] = PlayerMLeagueResult(
                rank=current_rank,
                score=score,
                point=round(point, 1),
            )

        return MLeagueScoreResult(players=players_result)