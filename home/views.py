from django.shortcuts import render
import requests
from home.tests_pokeapi import return_pokemon_data

# Create your views here.



def home(request):

    pokemons = return_pokemon_data()

    return render(request, 'pokedex.html', {'pokemons': pokemons})


def pokemon_detail(request, pokemon_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
    data = response.json()

    pokemon = {
        'id': data['id'],
        'name': data['name'],
        'sprite_url': data['sprites']['front_default'],
        'types': [t['type']['name'] for t in data['types']],
        'height': data['height'],
        'weight': data['weight'],
    }
    return render(request, 'pokemon_detail.html', {'pokemon': pokemon})