from pydantic import BaseModel
from typing import List, Optional, Dict

class PokemonBattle(BaseModel):
    pokemon_a: str
    pokemon_b: str


class BattleResult(BaseModel):
    status: str
    result: Optional[Dict] = None


class PokemonListResponse(BaseModel):
    pokemons: list
    page: int
    limit: int