import pytest
from fastapi import BackgroundTasks
from unittest.mock import Mock
from apps.controllers.pokemon_controller import list_pokemons, start_battle, get_battle_result
from apps.schemas.pokemon_schema import PokemonBattle 


@pytest.fixture
def mock_pokemon_data(monkeypatch):
    mock_data = {
        "pikachu": {"name": "Pikachu", "type1": "electric", "type2": "", "attack": "55"},
        "bulbasaur": {"name": "Bulbasaur", "type1": "grass", "type2": "poison", "attack": "49"},
        "charmander": {"name": "Charmander", "type1": "fire", "type2": "", "attack": "52"},
        "squirtle": {"name": "Squirtle", "type1": "water", "type2": "", "attack": "48"},
        "jigglypuff": {"name": "Jigglypuff", "type1": "fairy", "type2": "", "attack": "45"},
        "meowth": {"name": "Meowth", "type1": "normal", "type2": "", "attack": "41"},
        "psyduck": {"name": "Psyduck", "type1": "water", "type2": "", "attack": "47"},
        "abra": {"name": "Abra", "type1": "psychic", "type2": "", "attack": "20"},
        "mankey": {"name": "Mankey", "type1": "fighting", "type2": "", "attack": "80"},
        "pidgey": {"name": "Pidgey", "type1": "normal", "type2": "flying", "attack": "45"},
        "machop": {"name": "Machop", "type1": "fighting", "type2": "", "attack": "70"},
        "geodude": {"name": "Geodude", "type1": "rock", "type2": "ground", "attack": "80"}
    }
    monkeypatch.setattr("apps.controllers.pokemon_controller.pokemon_data", mock_data)
    return mock_data

@pytest.mark.asyncio
async def test_list_pokemons(mock_pokemon_data):
    result = await list_pokemons(1, 2)
    assert len(result["pokemons"]) == 2
    assert "pikachu" in result["pokemons"]

@pytest.mark.asyncio
async def test_start_battle(mock_pokemon_data):
    mock_background_tasks = Mock(BackgroundTasks)
    
    # Use the correct Pydantic model here
    battle = PokemonBattle(pokemon_a="Mankey", pokemon_b="")
    
    result = await start_battle(battle, mock_background_tasks)  # Use await
    assert "battleId" in result



@pytest.mark.asyncio
async def test_get_battle_result(mock_pokemon_data):
    mock_background_tasks = Mock(BackgroundTasks)
    
    # Use the correct Pydantic model here
    battle = PokemonBattle(pokemon_a="pikachu", pokemon_b="bulbasaur")
    
    battle_id = (await start_battle(battle, mock_background_tasks))["battleId"]
    result = get_battle_result(battle_id)
    
    assert result["status"] in ["BATTLE_INPROGRESS", "BATTLE_COMPLETED"]