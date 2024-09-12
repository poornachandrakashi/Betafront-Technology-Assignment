from fastapi.testclient import TestClient
from run import app  # Importing FastAPI app from run.py
import pytest

client = TestClient(app)

@pytest.fixture
def mock_pokemon_data(monkeypatch):
    mock_data = {
        "pikachu": {"name": "Pikachu", "type1": "electric", "type2": "", "attack": "55"},
        "bulbasaur": {"name": "Bulbasaur", "type1": "grass", "type2": "poison", "attack": "49"}
    }
    monkeypatch.setattr("apps.controllers.pokemon_controller.pokemon_data", mock_data)
    return mock_data

def test_list_pokemons(mock_pokemon_data):
    response = client.get("/api/pokemon/list_pokemons?page=1&limit=5")
    assert response.status_code == 200
    assert "pokemons" in response.json()
    assert isinstance(response.json()["pokemons"], list)
    assert len(response.json()["pokemons"]) <= 5

def test_start_battle(mock_pokemon_data):
    response = client.post("/api/pokemon/battle/", json={"pokemon_a": "pikachu", "pokemon_b": "bulbasaur"})
    assert response.status_code == 200  # This should now pass

def test_battle_status_in_progress(mock_pokemon_data):
    # Start a battle
    response = client.post("/api/pokemon/battle/", json={"pokemon_a": "pikachu", "pokemon_b": "bulbasaur"})
    assert response.status_code == 200
    battle_id = response.json()["battleId"]

    # Immediately check status (it should be in progress)
    result_response = client.get(f"/api/pokemon/battle/{battle_id}")
    assert result_response.status_code == 200
    assert result_response.json()["status"] in ["BATTLE_INPROGRESS", "BATTLE_COMPLETED"]
