import pytest
from apps.controllers.utilities.pokemon_util import calculate_damage
from apps.models.pokemon_model import Pokemon  # Ensure you're importing the Pokemon model

# Mock Pokémon data as instances of the Pokemon class
@pytest.fixture
def mock_pokemon_data():
    return {
        "charmander": Pokemon("Charmander", {"type1": "fire", "type2": "", "attack": "52"}),
        "squirtle": Pokemon("Squirtle", {"against_fire": "0.5", "against_water": "2", "attack": "44"})
    }

def test_calculate_damage(mock_pokemon_data):
    pokemon_a = mock_pokemon_data["charmander"]
    pokemon_b = mock_pokemon_data["squirtle"]

    damage_a_to_b = calculate_damage(pokemon_a, pokemon_b)
    assert damage_a_to_b > 0

    damage_b_to_a = calculate_damage(pokemon_b, pokemon_a)
    assert damage_b_to_a > 0
