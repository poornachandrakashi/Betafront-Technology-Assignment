import pytest
from unittest.mock import Mock
from fastapi import BackgroundTasks
from apps.controllers.pokemon_controller import BattleSimulator, PokemonController
from apps.schemas.pokemon_schema import PokemonBattle

@pytest.mark.asyncio
async def test_start_battle(mock_pokemon_data):
    mock_background_tasks = Mock(BackgroundTasks)
    
    # Simulate starting a battle with the modified instance
    battle_simulator = BattleSimulator()
    pokemon_controller = PokemonController(mock_pokemon_data, battle_simulator)
    
    battle = PokemonBattle(pokemon_a="pikachu", pokemon_b="bulbasaur")
    result = await pokemon_controller.start_battle(battle.dict(), mock_background_tasks)
    assert "battleId" in result

@pytest.mark.asyncio
async def test_get_battle_result(mock_pokemon_data):
    mock_background_tasks = Mock(BackgroundTasks)
    
    battle_simulator = BattleSimulator()
    pokemon_controller = PokemonController(mock_pokemon_data, battle_simulator)
    
    battle = PokemonBattle(pokemon_a="pikachu", pokemon_b="bulbasaur")
    battle_id = (await pokemon_controller.start_battle(battle.dict(), mock_background_tasks))["battleId"]
    
    result = pokemon_controller.get_battle_result(battle_id)
    assert result["status"] in ["BATTLE_INPROGRESS", "BATTLE_COMPLETED"]
