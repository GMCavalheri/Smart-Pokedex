import requests
import json

def get_pokemon_data(name_or_id):
    # Ensure the input name is lowercase
    url = f"https://pokeapi.co/api/v2/pokemon/{str(name_or_id).lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Could not retrieve data (Status Code: {response.status_code})")
        return None



def return_pokemon_data():
    
    pokemons = []

    for p in range(1,152):

        pokemon_data = get_pokemon_data(p)

        pokemon = {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'],
        'sprite_url': pokemon_data['sprites']['front_default'],
        'types': [t['type']['name'] for t in pokemon_data['types']],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        }

        pokemons.append(pokemon)


    return pokemons



