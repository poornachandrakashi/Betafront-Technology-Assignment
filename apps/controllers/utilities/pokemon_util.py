import time
import os
from typing import Dict

def calculate_damage(pokemon_a: Dict[str, str], pokemon_b: Dict[str, str]) -> float:
    type1_a = pokemon_a.get('type1', None) 
    type2_a = pokemon_a.get('type2', None) 
    against_type1_b = 0
    against_type2_b = 0
    attack_a = int(pokemon_a.get('attack'),0)
    if type1_a is not None and type1_a != "":
        against_type1_b = float(pokemon_b.get(f'against_{type1_a}', 0))

    if type2_a is not None and type2_a != "":
        against_type2_b = float(pokemon_b.get(f'against_{type2_a}', 0))

    damage_reduction = 0

    if against_type1_b != 0:
        damage_reduction += (against_type1_b / 4) * 100

    if against_type2_b != 0:
        damage_reduction += (against_type2_b / 4) * 100
        
    damage = (attack_a / int(os.getenv("ATTACK_DIVISOR"))) * int(os.getenv("DAMAGE_MULTIPLIER")) - damage_reduction
    return max(damage, 0)