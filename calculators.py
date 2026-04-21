import math
from typing import Dict, List
from models import YAKU_MASTER, HandInput

class MahjongCalculator:
    
    #麻雀の点数計算を行うクラス
    
    def calculate_han_breakdown(self, hand_input: HandInput) -> Dict[str, int]:
        #役の内訳を計算するメソッド
        breakdown: Dict[str, int] = {}
        
        for yaku_name in hand_input.selected_yaku:
            yaku = YAKU_MASTER.get(yaku_name)
            if not yaku:
                continue
            
            han = yaku.han_closed if hand.is_menzen else yaku.han_open
            if han > 0:
                breakdown[yaku_name] = han
            
        if hand.dora_count > 0:
            breakdown["ドラ"] = hand.dora_count
        if hand.uradora_count > 0:
            breakdown["裏ドラ"] = hand.uradora_count
        if hand.akadara_count > 0:
            breakdown["赤ドラ"] = hand.akadara_count
            
        return breakdown
    
    def calculate_total_han(self, hand: HandInput) -> int:
        
        #合計翻数を計算するメソッド
        
        breakdown = self.calculate_han_breakdown(hand)
        return sum(breakdown.values())
    
    def is_chiitoitsu(self, hand: HandInput) -> bool:
        
        #七対子かどうかを判定するメソッド
        
        return "七対子" in hand.selected_yaku
    
    def validate_hand(self, hand: HandInput) -> List[str]:
        
        #手牌の入力が正しいかを検証するメソッド
        
        errors: List[str] = []
        
        if len(hand.selected_yaku) == 0 and (
            hand.dora_count + hand.uradora_count + hand.akadara_count == 0
            ):
            errors.append("役またはドラが選択されていません。")
        
        if self.is_chiitoitsu(hand) and hand.fu != 25:
            errors.append("七対子の場合、符は25が固定です。")
        
        closed_only_yaku = {
            "立直", "一発", "門前清自摸和", "一盃口", "二盃口","平和"
        }
        if not hand.is_menzed:
            invalid_yaku = sorted(set(hannd.selected_yaku) & closed_only_yaku)
            if invalid_yaku:
                errors.append(f"鳴きありの場合、以下の役は選択できません: {', '.join(invalid_yaku)}"
                              )
        return errors

    def calculate_base_points(self, fu: int, han: int) -> int:
        
        #基本点を計算するメソッド
        
        if han <= 0:
            return 0
        
        if han >= 13:
            return 8000 #数え役満
        if han >= 11:
            return 6000 #3倍満
        if han >= 8:
            return 4000 #倍満
        if han >= 6:
            return 3000 #跳満
        if han >= 5:
            return 2000 #満貫
        
        raw_base = fu * (2 ** (han + 2))
        if raw_base >= 2000:
            return 2000 #満貫以上は基本点2000で固定        
        
        return raw_base
    
    @staticmethod
    def round_up_to_100(values: int) -> int:
        
        #点数を100点単位に切り上げるメソッド
        
        return int(math.ceil(values / 100.0) * 100)
    
    def calculate_score(self, hand: HandInput) -> Dict[str, int]:
        
        #最終的な点数を計算するメソッド
        
        total_han = self.calculate_total_han(hand)
        fu = hand.fu
        base_points = self.calculate_base_points(fu, total_han)
    
        result: Dict[str, int | str] = {
        "han": total_han,
        "fu": fu,
        "base_points": base_points,
        "honba": hand.honba,
        "riichi_sticks": hand.riichi_sticks,
        }
    
        if total_han == 0:
            result["label"] = "役なし"
            result["score"] = 0
            return result
        
        if hand.is_tsumo:
            if hand.is_oya:
                payment = self.round_up_to_100(base_points * 2)
                total = payment * 3 + hand.honba * 300 + hand.riichi_sticks * 1000
                result["label"] = f"親のツモ {payment}オール"
                result["score"] = total
            else:
                child_payment = self.round_up_to_100(base_points)
                dealer_payment = self.round_up_to_100(base_points * 2)
                total = (
                    child_payment * 2 + 
                    dealer_payment +
                    hand.honba * 300 + 
                    hand.riichi_sticks * 1000
                )
                result["label"] = f"子ツモ 子:{child_payment} / 親:{dealer_payment}"
                result["score"] = total
        
        else:
                multiplier = 6 if hand.is_oya else 4
                ron_score = self.round_up_to_100(base_points * multiplier)
                total = ron_score + hand.honba * 300 + hand.riichi_sticks * 1000
                result["label"] = "親ロン" if hand.is_oya else "子ロン"
                result["ron_points"] = ron_score
                result["total_points"] = total

        return result
        
    def get_score_title(self, han:int, base_points: int) -> str:
        
        #点数のタイトルを取得するメソッド
        
        if han >= 13:
            return "数え役満"
        if han >= 11:
            return "3倍満"
        if han >= 8:
            return "倍満"
        if han >= 6:
            return "跳満"
        if han >= 5 or base_points >= 2000:
            return "満貫"
        return f"{han}翻 {base_points}点"