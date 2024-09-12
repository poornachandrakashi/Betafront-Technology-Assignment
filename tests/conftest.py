import pytest
from fastapi.testclient import TestClient
from run import app
from apps.controllers.pokemon_controller import PokemonDataManager
from apps.core.logger import logger


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_pokemon_data_manager():
    class MockPokemonDataManager(PokemonDataManager):
        def __init__(self):
            super().__init__()
            logger.debug("===============================LINE 15")
            self.load_pokemon_data() 

        def load_pokemon_data(self):
            super().load_pokemon_data()  

    return MockPokemonDataManager()

@pytest.fixture(autouse=False)
def override_pokemon_data_manager(mock_pokemon_data_manager):
    app.dependency_overrides[PokemonDataManager] = lambda: mock_pokemon_data_manager
    yield
    app.dependency_overrides = {} 
