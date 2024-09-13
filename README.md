
# Pokemon Battle

The Pokémon Battle is a backend project built using FastAPI. The users can do below steps:
List Pokémon names with pagination.
Start a battle between two Pokémon asynchronously.
Retrieve battle results once the battle is completed using the battle id.
The project involves loading Pokémon data from a CSV file downloaded from Kaggle dataset, running a simulation of battles based on Pokémon types and attack values, and returning results via API endpoints.


## Low Level Design
```
Client
   |
   v
  (1) Start Battle Request: POST /api/pokemon/battle
   |
   v
 FastAPI App (Data is preloaded at startup)
   |
   v
Routes Module (Battle Start Endpoint)
   |
   v
Controller Module
   |------------------------------|
   |                              |
   v                              v
 Preloaded Pokémon Data  Utilities (calculate_damage)
 (In-memory from CSV)   (Simulates battle using loaded data)
   |
   v
 If successful: Store battle result in-memory
 If failed: Mark battle as failed and return failure status
   |
   v
Respond with Battle ID: {"battleId": "123e4567-e89b-12d3-a456-426614174000"}
   |
   v
Client (Receives Battle ID)
   |
   v
  (2) Poll Status: GET /api/pokemon/battle/{battle_id}
   |
   v
Routes Module (Battle Status Endpoint)
   |
   v
Controller Module (Checks battle status)
   |
   v
  (a) If battle is in progress:
     Response: {"status": "BATTLE_INPROGRESS", "result": null}
   |
   v
  (b) If battle is completed:
     Response: {
       "status": "BATTLE_COMPLETED",
       "result": {"winnerName": "pikachu", "wonByMargin": 12.5}
     }
   |
   v
  (c) If battle failed:
     Response: {
       "status": "BATTLE_FAILED",
       "result": null
     }

```




## API Reference

#### Get list of pokemons

```http
  GET /api/pokemon/list_pokemons
```

To list the pokemons listed in the csv file.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `page` | `int` | Page number for pagination (default is 1). |
| `limit`| `int` | Number of Pokémon per page (default is 10).|

#### Start the battle

```http
  POST /api/pokemon/battle
```
To start the battle between two pokemons.

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pokemon_a`      | `string` | **Required**. Name of the first Pokémon. |
|`pokemon_b`|`string`|**Required**.Name of the second Pokémon.|

#### Get Battle Status/Result

```http
  GET /api/pokemon/battle/{id}
```
To check the status of the battle. 

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` |**Required** Battle Id |


## Running Pokémon Battle

##prerequisities
* Python 3.8+
* Pip
* Git


### Clone the repository from github

```
git clone 
```
### Move to the directory and create virtualenv

```
cd 
```

```
python -m venv .venv
```
or 

```
python3 -m venv .venv
```

### Activate Virtual env

#### For Windows
```
.venv\Scripts\activate
```

### Install neccessary dependency using requirements.txt

```
pip install -r requirements.txt
```


### Run the project

```
python run.py
```

or 

```
python3 run.py
```

## Unit Testing Pokémon Battle

Set the project directory in the environment variable

```
set PYTHONPATH=C:\Poorna\Projects\Assignments\betfront-assignment
```

Like the above , please set whatever is the path in your cmd line.


Then run the below command.

```
pytest --asyncio-mode=auto --cov=apps tests/
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```
ATTACK_DIVISOR = 200
DAMAGE_MULTIPLIER = 100
```