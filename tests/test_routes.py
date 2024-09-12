import pytest
from fastapi.testclient import TestClient
from run import app
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_pokemon_data(monkeypatch):
    from apps.controllers.pokemon_controller import PokemonDataManager
    from apps.models.pokemon_model import Pokemon

    class MockPokemonDataManager(PokemonDataManager):
        def __init__(self):
            self.pokemon_data = {
                "pikachu": Pokemon("pikachu", {"type1": "electric", "attack": 55, "defense": 40}),
                "bulbasaur": Pokemon("bulbasaur", {"type1": "grass", "type2": "poison", "attack": 49, "defense": 49})
            }

        def load_pokemon_data(self):
            logger.debug("Mock load_pokemon_data called")

        def get_pokemon(self, name: str):
            pokemon = self.pokemon_data.get(name.lower())
            logger.debug(f"get_pokemon called with {name}, returned {pokemon}")
            return pokemon

    monkeypatch.setattr("apps.controllers.pokemon_controller.PokemonDataManager", MockPokemonDataManager)
    logger.debug("MockPokemonDataManager set up")

@pytest.mark.usefixtures("mock_pokemon_data")
class TestPokemonRoutes:
    def test_list_pokemons(self, client):
        response = client.get("/api/pokemon/list_pokemons?page=1&limit=5")
        logger.debug(f"list_pokemons response: {response.text}")
        assert response.status_code == 200
        assert "pokemons" in response.json()
        assert isinstance(response.json()["pokemons"], list)
        assert len(response.json()["pokemons"]) <= 5

    def test_start_battle(self, client):
        payload = {"pokemon_a": "pikachu", "pokemon_b": "bulbasaur"}
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = client.post("/api/pokemon/battle/", json=payload, headers=headers)
        logger.debug(f"start_battle response: {response.text}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        assert "battleId" in response.json()

    def test_battle_status_in_progress(self, client):
        # Start a battle
        response = client.post("/api/pokemon/battle/", json={"pokemon_a": "pikachu", "pokemon_b": "bulbasaur"})
        logger.debug(f"start_battle response: {response.text}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        battle_id = response.json()["battleId"]

        # Check the battle status
        result_response = client.get(f"/api/pokemon/battle/{battle_id}")
        logger.debug(f"battle_status response: {result_response.text}")
        assert result_response.status_code == 200
        assert result_response.json()["status"] in ["BATTLE_INPROGRESS", "BATTLE_COMPLETED"]

def test_mock_pokemon_data(mock_pokemon_data):
    # This test is to verify that our mock is working correctly
    from apps.controllers.pokemon_controller import PokemonDataManager
    pdm = PokemonDataManager()
    assert pdm.get_pokemon("pikachu") is not None
    assert pdm.get_pokemon("bulbasaur") is not None
    assert pdm.get_pokemon("nonexistent") is None