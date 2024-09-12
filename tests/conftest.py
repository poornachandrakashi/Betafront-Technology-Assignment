import pytest
from apps.controllers.pokemon_controller import PokemonDataManager

@pytest.fixture
def mock_pokemon_data(monkeypatch):
    # Create mock Pokémon data
    mock_data = {
        "pikachu": {"name": "Pikachu", "type1": "electric", "type2": "", "attack": "55"},
        "bulbasaur": {"name": "Bulbasaur", "type1": "grass", "type2": "poison", "attack": "49"}
    }

    # Create an instance of PokemonDataManager
    instance = PokemonDataManager()

    # Patch the instance's pokemon_data with mock data
    monkeypatch.setattr(instance, 'pokemon_data', mock_data)

    # Return the modified instance
    return instance
