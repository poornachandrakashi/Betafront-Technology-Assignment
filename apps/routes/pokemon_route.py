from fastapi import BackgroundTasks, Depends, APIRouter, Query
from apps.controllers import pokemon_controller
from apps.schemas.pokemon_schema import PokemonBattle, PokemonListResponse

pokemon_router = APIRouter(
    prefix="/api/pokemon",
)

@pokemon_router.on_event("startup")
def loading_pokemon_data():
    return pokemon_controller.load_pokemon_data()

@pokemon_router.get("/list_pokemons", response_model=PokemonListResponse)
async def list_pokemon(page: int = Query(1, alias="page"), limit: int = Query(10, alias="limit")):
    return await pokemon_controller.list_pokemons(page,limit)

@pokemon_router.post("/battle/")
async def start_pokemon_battle(battle: PokemonBattle,background_tasks: BackgroundTasks):
    return await pokemon_controller.start_battle(battle,background_tasks)

@pokemon_router.get("/battle/{battle_id}")
def pokemon_battle_status(battle_id:str):
    return pokemon_controller.get_battle_result(battle_id)