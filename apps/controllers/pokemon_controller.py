import csv
import time
import uuid
from typing import Dict, List, Optional
from fastapi import BackgroundTasks, HTTPException
from apps.controllers.utilities.pokemon_util import calculate_damage, check_spelling
from apps.core.logger import logger
from apps.models.pokemon_model import Pokemon

class BattleResult:
    def __init__(self, battle_id: str):
        self.battle_id = battle_id
        self.status = "BATTLE_INPROGRESS"
        self.result = None

    def set_completed(self, winner: str, margin: float):
        self.status = "BATTLE_COMPLETED"
        self.result = {"winnerName": winner, "wonByMargin": margin}

    def set_failed(self):
        self.status = "BATTLE_FAILED"
        self.result = None

class PokemonDataManager:
    def __init__(self, csv_file: str = 'pokemon.csv'):
        self.pokemon_data: Dict[str, Pokemon] = {}

    def load_pokemon_data(self):
        try:
            logger.debug("Loading Pokémon data from CSV file.")
            with open('pokemon.csv', mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if 'name' in row and row['name'].strip():
                        pokemon_name = row['name'].strip().lower()
                        self.pokemon_data[pokemon_name] = Pokemon(pokemon_name, row)
                    else:
                        logger.error(f"Invalid row in CSV: {row}")
            logger.info(f"Loaded {len(self.pokemon_data)} Pokémon from pokemon.csv")
        except FileNotFoundError:
            logger.error("File 'pokemon.csv' not found.")
        except Exception as e:
            logger.error(f"Error loading Pokémon data: {e}")


    def get_pokemon(self, name: str) -> Optional[Pokemon]:
        return self.pokemon_data.get(name.lower().strip()) 

    def list_pokemons(self, page: int, limit: int) -> List[str]:
        start = (page - 1) * limit
        end = start + limit

        return list(self.pokemon_data.keys())[start:end]


class BattleSimulator:
    def __init__(self):
        self.battle_results: Dict[str, BattleResult] = {}

    def simulate_battle(self, pokemon_a: Pokemon, pokemon_b: Pokemon, battle_id: str):
        try:
            time.sleep(5) 
            damage_a_to_b = calculate_damage(pokemon_a, pokemon_b)
            damage_b_to_a = calculate_damage(pokemon_b, pokemon_a)

            if damage_a_to_b > damage_b_to_a:
                winner = pokemon_a.name
                margin = damage_a_to_b - damage_b_to_a
            elif damage_b_to_a > damage_a_to_b:
                winner = pokemon_b.name
                margin = damage_b_to_a - damage_a_to_b
            else:
                winner = "Draw"
                margin = 0

            self.battle_results[battle_id].set_completed(winner, margin)
        except Exception as e:
            self.battle_results[battle_id].set_failed()
            logger.error(f"Battle simulation failed: {e}")

    def start_battle(self, pokemon_a_name: str, pokemon_b_name: str, pokemon_data_manager: PokemonDataManager, background_tasks: BackgroundTasks):
        battle_id = str(uuid.uuid4())

        logger.debug(pokemon_a_name)

        logger.debug(pokemon_b_name)
        pokemon_a = pokemon_data_manager.get_pokemon(pokemon_a_name)
        pokemon_b = pokemon_data_manager.get_pokemon(pokemon_b_name)


        logger.debug(pokemon_a)

        logger.debug("======================================LINE 88")
        if not pokemon_a or not pokemon_b:
            raise HTTPException(status_code=400, detail="Invalid Pokémon name")

        battle_result = BattleResult(battle_id)
        self.battle_results[battle_id] = battle_result

        background_tasks.add_task(self.simulate_battle, pokemon_a, pokemon_b, battle_id)
        return battle_id

    # def start_battle(self, pokemon_a_name: str, pokemon_b_name: str, pokemon_data_manager: PokemonDataManager, background_tasks: BackgroundTasks):
    #     battle_id = str(uuid.uuid4())
    #     from fuzzywuzzy import process
    #     def fuzzy_match_pokemon(name):
    #         matches = process.extract(name, pokemon_data_manager.pokemon_data.keys(), limit=3)
    #         exact_match = next((match for match in matches if match[1] == 100), None)
    #         if exact_match:
    #             return pokemon_data_manager.get_pokemon(exact_match[0])
            
    #         close_matches = [match for match in matches if match[1] >= 80]
    #         if len(close_matches) == 1:
    #             logger.info(f"Accepted close match: {close_matches[0][0]} for input {name}")
    #             if check_spelling(close_matches[0][0],name):
    #                 return pokemon_data_manager.get_pokemon(close_matches[0][0])
                
    #         raise HTTPException(status_code=400, detail="Invalid Pokémon name")

    #     pokemon_a = fuzzy_match_pokemon(pokemon_a_name)
    #     pokemon_b = fuzzy_match_pokemon(pokemon_b_name)

    #     logger.debug(f"Matched Pokemon A: {pokemon_a}")
    #     logger.debug(f"Matched Pokemon B: {pokemon_b}")

    #     logger.debug("======================================LINE 88")
    #     # if not pokemon_a or not pokemon_b:
    #     #     raise HTTPException(status_code=400, detail="Invalid Pokémon name")

    #     battle_result = BattleResult(battle_id)
    #     self.battle_results[battle_id] = battle_result

    #     background_tasks.add_task(self.simulate_battle, pokemon_a, pokemon_b, battle_id)
    #     return battle_id

    def get_battle_result(self, battle_id: str) -> Dict:
        result = self.battle_results.get(battle_id)
        if not result:
            return {"status": "BATTLE_INPROGRESS", "result": None}
        return {"status": result.status, "result": result.result}

class PokemonController:
    def __init__(self, data_manager: PokemonDataManager, battle_simulator: BattleSimulator):
        self.data_manager = data_manager
        self.battle_simulator = battle_simulator

    async def list_pokemons(self, page: int, limit: int):
        pokemons = self.data_manager.list_pokemons(page, limit)

        logger.debug("======================================LINE 112")
        logger.debug(pokemons)
        return {"pokemons": pokemons, "page": page, "limit": limit}

    async def start_battle(self, battle: dict, background_tasks: BackgroundTasks):
        battle_id = self.battle_simulator.start_battle(battle['pokemon_a'], battle['pokemon_b'], self.data_manager, background_tasks)
        return {"battleId": battle_id}

    def get_battle_result(self, battle_id: str):
        return self.battle_simulator.get_battle_result(battle_id)
