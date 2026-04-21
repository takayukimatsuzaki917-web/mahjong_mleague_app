from dataclasses import dataclass
from typing import Dict, List

@dataclass (frozen=True)
class Yaku:
    
    #一つの役の情報を保持するクラス
    name: str
    han_closed: int
    han_open: int
    
YAKU_MASTER: Dict[str, Yaku] = {
    "立直": Yaku("立直", 1, 1),
    "一発": Yaku("一発", 1, 0),
    "門前清自摸和": Yaku("門前清自摸和", 1, 0),
    "断么九": Yaku("断么九", 1, 1),
    "一盃口": Yaku("一盃口", 1, 0),
    "平和": Yaku("平和", 1, 0),
    "自風牌": Yaku("自風牌", 1, 1),
    "場風牌": Yaku("場風牌", 1, 1),
    "役牌": Yaku("役牌", 1, 1),
    "二盃口": Yaku("二盃口", 3, 0),
    "三色同順": Yaku("三色同順", 2, 1),
    "三色同刻": Yaku("三色同刻", 2, 2),
    "三槓子": Yaku("三槓子", 2, 2),
    "対々和": Yaku("対々和", 2, 2),
    "三暗刻": Yaku("三暗刻", 2, 2),
    "小三元": Yaku("小三元", 2, 2),
    "混全帯么九": Yaku("混全帯么九", 2, 1),
    "純全帯么九": Yaku("純全帯么九", 3, 2),
    "混老頭": Yaku("混老頭", 2, 2),
    "四暗刻": Yaku("四暗刻", 13, 13),
    "国士無双": Yaku("国士無双", 13, 13),
    "小四喜": Yaku("小四喜", 13, 13),
    "大四喜": Yaku("大四喜", 13, 13),
    "字一色": Yaku("字一色", 13, 13),
    "清老頭": Yaku("清老頭", 13, 13),
    "四槓子": Yaku("四槓子", 13, 13),
    "九蓮宝燈": Yaku("九蓮宝燈", 13, 13),
    "純正九蓮宝燈": Yaku("純正九蓮宝燈", 13, 13),
    "国士無双十三面待ち": Yaku("国士無双十三面待ち", 13, 13),
    "大三元": Yaku("大三元", 13, 13),
    "清一色": Yaku("清一色", 6, 5),
    "混一色": Yaku("混一色", 3, 2),
}

@dataclass
class HandInput:
    
    #ユーザーからの入力を保持するクラス
    selected_yaku: List[str]
    is_tsumo: bool
    is_menzen: bool
    is_oya: bool
    fu: int
    honba: int = 0
    riichi_sticks: int = 0
    dors_count: int = 0
    ura_dors_count: int = 0
    aka_dors_count: int = 0