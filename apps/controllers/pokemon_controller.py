import csv
import time
from typing import Dict
import uuid
from fastapi import BackgroundTasks, HTTPException
from starlette.responses import FileResponse, JSONResponse
from apps.controllers.utilities.pokemon_util import calculate_damage
from apps.core.logger import logger
from apps.core.util import response_json

pokemon_data = {}
battle_results: Dict[str, Dict] = {}

def load_pokemon_data():
    global pokemon_data
    try:
        with open('pokemon.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if 'name' in row and row['name'].strip():
                    pokemon_data[row['name'].strip().lower()] = row
                else:
                    logger.error(f"Invalid row in CSV: {row}")
        logger.info(f"Loaded {len(pokemon_data)} Pokémon from pokemon.csv")
    except FileNotFoundError:
        logger.error(f"File 'pokemon.csv' not found.")
    except Exception as e:
        logger.error(f"Error loading Pokémon data: {e}")

async def list_pokemons(page, limit):
    start = (page - 1) * limit
    end = start + limit
    pokemons = list(pokemon_data.keys())[start:end]
    return {"pokemons": pokemons, "page": page, "limit": limit}


def simulate_battle(pokemon_a_name, pokemon_b_name, battle_id): 
    try:
        time.sleep(5)    
        pokemon_a = pokemon_data.get(pokemon_a_name.lower())
        pokemon_b = pokemon_data.get(pokemon_b_name.lower())

        if not pokemon_a or not pokemon_b:
            logger.info("Battle failed as one of the pokemon details are not available in csv sheet")
            battle_results[battle_id] = {
                "status": "BATTLE_FAILED",
                "result": None
            }
            return

        damage_a_to_b = calculate_damage(pokemon_a, pokemon_b)
        damage_b_to_a = calculate_damage(pokemon_b, pokemon_a)

        if damage_a_to_b > damage_b_to_a:
            winner = pokemon_a['name']
            margin = damage_a_to_b - damage_b_to_a
        elif damage_b_to_a > damage_a_to_b:
            winner = pokemon_b['name']
            margin = damage_b_to_a - damage_a_to_b
        else:
            winner = "Draw"
            margin = 0

        battle_results[battle_id] = {
            "status": "BATTLE_COMPLETED",
            "result": {
                "winnerName": winner,
                "wonByMargin": margin
            }
        }
    except Exception as e:
        battle_results[battle_id] = {
            "status": "BATTLE_FAILED",
            "result": None
        }
        logger.error(e)

async def start_battle(battle,background_tasks):
    pokemon_a = battle.pokemon_a
    pokemon_b = battle.pokemon_b
    battle_id = str(uuid.uuid4())

    if pokemon_a.lower() not in pokemon_data or pokemon_b.lower() not in pokemon_data:
        raise HTTPException(status_code=400, detail="Invalid Pokémon name")
    
    background_tasks.add_task(simulate_battle, pokemon_a, pokemon_b, battle_id)
    return {"battleId": battle_id}

def get_battle_result(battle_id):
    print(battle_results)
    print("===================BATTLE RESULTS========================")
    result = battle_results.get(battle_id)
    if not result:
        return {"status": "BATTLE_INPROGRESS", "result": None}
    return result

