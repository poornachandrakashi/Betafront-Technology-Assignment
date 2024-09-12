from fastapi import BackgroundTasks, Depends, APIRouter, Query
from apps.controllers.pokemon_controller import PokemonController
from apps.schemas.pokemon_schema import PokemonBattle, PokemonListResponse

# Initialize PokemonDataManager and BattleSimulator for controller use
from apps.controllers.pokemon_controller import PokemonDataManager, BattleSimulator

pokemon_data_manager = PokemonDataManager()
battle_simulator = BattleSimulator()
pokemon_controller = PokemonController(data_manager=pokemon_data_manager, battle_simulator=battle_simulator)

pokemon_router = APIRouter(
    prefix="/api/pokemon",
)

@pokemon_router.on_event("startup")
def loading_pokemon_data():
    """Load Pokémon data when the application starts."""
    return pokemon_data_manager.load_pokemon_data()

@pokemon_router.get("/list_pokemons", response_model=PokemonListResponse)
async def list_pokemon(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    """Fetch Pokémon with pagination."""
    return await pokemon_controller.list_pokemons(page, limit)

@pokemon_router.post("/battle/")
async def start_pokemon_battle(battle: PokemonBattle, background_tasks: BackgroundTasks):
    """Initiate a battle between two Pokémon."""
    return await pokemon_controller.start_battle(battle.dict(), background_tasks)

@pokemon_router.get("/battle/{battle_id}")
def pokemon_battle_status(battle_id: str):
    """Check the status and result of a Pokémon battle."""
    return pokemon_controller.get_battle_result(battle_id)
