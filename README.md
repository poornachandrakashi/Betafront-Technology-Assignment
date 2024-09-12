
# Pokemon Battle

The Pokémon Battle is a backend project built using FastAPI. The users can do below steps:
List Pokémon names with pagination.
Start a battle between two Pokémon asynchronously.
Retrieve battle results once the battle is completed using the battle id.
The project involves loading Pokémon data from a CSV file downloaded from Kaggle dataset, running a simulation of battles based on Pokémon types and attack values, and returning results via API endpoints.

## Deployment Pokémon Battle

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

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```
ATTACK_DIVISOR = 200
DAMAGE_MULTIPLIER = 100
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

