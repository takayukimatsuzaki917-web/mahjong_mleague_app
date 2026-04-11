from dataclasses import dataclass
from enum import Enum


# 親か子かを表す
class WinnerType(str, Enum):
    DEALER = "親"
    NON_DEALER = "子"


# ロンかツモかを表す
class WinType(str, Enum):
    RON = "ロン"
    TSUMO = "ツモ"


# 和了点計算に使う入力データ
@dataclass(frozen=True)
class HandInput:
    fu: int
    han: int  # ここでは「役の翻数（場ゾロ抜き）」を入れる想定
    winner_type: WinnerType
    win_type: WinType
    honba: int = 0
    kyotaku: int = 0
    include_bazoro: bool = True  # Trueなら場ゾロ2翻を自動加算


# 和了点計算の結果を入れる箱
@dataclass(frozen=True)
class HandResult:
    base_points: int
    total_points: str
    rounded_points: int | None = None
    dealer_payment: int | None = None
    non_dealer_payment: int | None = None


# Mリーグ最終ポイント計算に使う入力データ
@dataclass(frozen=True)
class MLeagueScoreInput:
    scores: list[int]  # 4人分の素点
    riichi_sticks_on_table: int = 0


# 各プレイヤーの計算結果
@dataclass(frozen=True)
class PlayerMLeagueResult:
    rank: int
    score: int
    point: float


# 4人分の結果全体
@dataclass(frozen=True)
class MLeagueScoreResult:
    players: list[PlayerMLeagueResult]