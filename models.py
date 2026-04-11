from dataclasses import dataclass
from enum import Enum


class WinnerType(str, Enum):
    DEALER = "親"
    NON_DEALER = "子"


class WinType(str, Enum):
    RON = "ロン"
    TSUMO = "ツモ"


@dataclass(frozen=True)
class HandInput:
    fu: int
    han: int  # ここでは「役の翻数」を入力する想定
    winner_type: WinnerType
    win_type: WinType
    honba: int = 0
    kyotaku: int = 0
    include_bazoro: bool = True  # Mリーグ向けに場ゾロ2翻を加える