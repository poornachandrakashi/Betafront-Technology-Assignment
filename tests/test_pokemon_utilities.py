import pytest
from apps.controllers.utilities.pokemon_util import calculate_damage, check_spelling
from apps.models.pokemon_model import Pokemon 

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

def test_check_spelling_exact_match():
    assert check_spelling("Charmander", "Charmander") == True

def test_check_spelling_case_insensitive():
    assert check_spelling("Charmander", "charmander") == True

def test_check_spelling_one_character_difference():
    assert check_spelling("Charmander", "Charmender") == True

def test_check_spelling_missing_one_character():
    assert check_spelling("Charmander", "Charmaner") == True

def test_check_spelling_extra_one_character():
    assert check_spelling("Charmander", "Charzmander") == True

