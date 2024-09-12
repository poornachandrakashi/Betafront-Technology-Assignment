import time
import os
from typing import Optional
from apps.models.pokemon_model import Pokemon

def calculate_damage(pokemon_a: Pokemon, pokemon_b: Pokemon) -> float:
    """Calculates the damage dealt by pokemon_a to pokemon_b."""
    
    # Get Pokémon A's attack types and values
    type1_a = pokemon_a.type1 or None
    type2_a = pokemon_a.type2 or None
    attack_a = pokemon_a.attack
    
    # Default values for defense of Pokémon B
    against_type1_b = 0.0
    against_type2_b = 0.0

    # Get Pokémon B's defense against Pokémon A's types
    if type1_a:
        against_type1_b = float(pokemon_b.__dict__.get(f'against_{type1_a}', 0.0))

    if type2_a:
        against_type2_b = float(pokemon_b.__dict__.get(f'against_{type2_a}', 0.0))

    # Calculate total damage reduction based on defenses
    damage_reduction = 0.0
    if against_type1_b:
        damage_reduction += (against_type1_b / 4) * 100
    if against_type2_b:
        damage_reduction += (against_type2_b / 4) * 100

    # Handle missing environment variables
    attack_divisor = int(os.getenv("ATTACK_DIVISOR", 200))
    damage_multiplier = int(os.getenv("DAMAGE_MULTIPLIER", 100))

    # Calculate the damage dealt by Pokémon A to Pokémon B
    damage = (attack_a / attack_divisor) * damage_multiplier - damage_reduction
    return max(damage, 0.0)  # Ensure that damage is not negative
