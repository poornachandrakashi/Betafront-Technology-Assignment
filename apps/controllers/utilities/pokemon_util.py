import time
import os
from typing import Optional
from apps.models.pokemon_model import Pokemon

def calculate_damage(pokemon_a: Pokemon, pokemon_b: Pokemon) -> float:
    type1_a = pokemon_a.type1 or None
    type2_a = pokemon_a.type2 or None
    attack_a = pokemon_a.attack
    against_type1_b = 0.0
    against_type2_b = 0.0

    if type1_a:
        against_type1_b = float(pokemon_b.__dict__.get(f'against_{type1_a}', 0.0))

    if type2_a:
        against_type2_b = float(pokemon_b.__dict__.get(f'against_{type2_a}', 0.0))

    damage_reduction = 0.0
    if against_type1_b:
        damage_reduction += (against_type1_b / 4) * 100
    if against_type2_b:
        damage_reduction += (against_type2_b / 4) * 100

    attack_divisor = int(os.getenv("ATTACK_DIVISOR", 200))
    damage_multiplier = int(os.getenv("DAMAGE_MULTIPLIER", 100))

    damage = (attack_a / attack_divisor) * damage_multiplier - damage_reduction
    return max(damage, 0.0)  

# def check_spelling(string1, string2):
#     string1 = string1.lower()
#     string2 = string2.lower()
    
#     if abs(len(string1) - len(string2)) > 1:
#         return False
    
#     i, j = 0, 0
#     differences = 0
    
#     while i < len(string1) and j < len(string2):
#         if string1[i] != string2[j]:
#             differences += 1
#             if differences > 1:
#                 return False
#             if len(string1) > len(string2):
#                 i += 1
#             elif len(string2) > len(string1):
#                 j += 1
#             else:
#                 i += 1
#                 j += 1
#         else:
#             i += 1
#             j += 1

#     if i < len(string1) or j < len(string2):
#         differences += 1

#     return differences <= 1