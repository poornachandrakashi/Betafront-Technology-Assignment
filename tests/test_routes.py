import pytest
from fastapi.testclient import TestClient
from run import app
from apps.controllers.pokemon_controller import PokemonDataManager

@pytest.fixture
def pokemon_data_manager():
    class TestPokemonDataManager(PokemonDataManager):
        def __init__(self):
            super().__init__()
            self.load_pokemon_data()  
    return TestPokemonDataManager()

@pytest.fixture
def client(pokemon_data_manager):
    app.dependency_overrides[PokemonDataManager] = lambda: pokemon_data_manager
    return TestClient(app)

class TestPokemonRoutes:

    def test_list_pokemons(self, client):
        response = client.get("/api/pokemon/list_pokemons?page=1&limit=20")
        assert response.status_code == 200
        pokemons = response.json().get("pokemons", [])
        assert len(pokemons) > 0  
        assert "pikachu" in pokemons
        assert "bulbasaur" in pokemons

    def test_start_battle(self, client):
        payload = {"pokemon_a": "pikachu", "pokemon_b": "bulbasaur"}
        response = client.post("/api/pokemon/battle/", json=payload)
        assert response.status_code == 200
        assert "battleId" in response.json()

    def test_battle_status_in_progress(self, client):
        response = client.post("/api/pokemon/battle/", json={"pokemon_a": "pikachu", "pokemon_b": "bulbasaur"})
        assert response.status_code == 200
        battle_id = response.json()["battleId"]
        result_response = client.get(f"/api/pokemon/battle/{battle_id}")
        assert result_response.status_code == 200
        assert result_response.json()["status"] in ["BATTLE_INPROGRESS", "BATTLE_COMPLETED"]
