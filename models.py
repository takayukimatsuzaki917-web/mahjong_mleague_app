# データをまとめるための便利な仕組み（クラスを簡単に書ける）
from dataclasses import dataclass

# 選択肢（親/子など）を固定するための仕組み
from enum import Enum


# 親か子かを表すクラス（Enum = 選択肢の集合）
class WinnerType(str, Enum):
    DEALER = "親"        # 親
    NON_DEALER = "子"   # 子


# ロンかツモかを表す
class WinType(str, Enum):
    RON = "ロン"        # ロン和了
    TSUMO = "ツモ"      # ツモ和了


# 入力データをまとめる箱
@dataclass(frozen=True)  # frozen=True → 値を変更できない（安全）
class HandInput:
    fu: int                 # 符
    han: int                # 翻
    winner_type: WinnerType # 親 or 子
    win_type: WinType       # ロン or ツモ
    honba: int = 0          # 本場（デフォルト0）
    kyotaku: int = 0        # 供託（デフォルト0）


# 計算結果をまとめる箱
@dataclass(frozen=True)
class HandResult:
    base_points: int             # 基本点
    total_points: str            # 表示用（例: 3900点）
    rounded_points: int | None = None  # ロンの時の点数
    dealer_payment: int | None = None  # 親の支払い
    non_dealer_payment: int | None = None  # 子の支払い


# 半荘終了時の入力
@dataclass(frozen=True)
class MLeagueScoreInput:
    scores: list[int]  # 4人の点数
    riichi_sticks_on_table: int = 0  # リーチ棒（今回は未使用）


# 各プレイヤーの結果
@dataclass(frozen=True)
class PlayerMLeagueResult:
    rank: int     # 順位
    score: int    # 素点
    point: float  # Mリーグポイント


# 全体の結果
@dataclass(frozen=True)
class MLeagueScoreResult:
    players: list[PlayerMLeagueResult]  # 4人分の結果