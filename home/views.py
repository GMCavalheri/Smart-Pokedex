from django.shortcuts import render

from pokedex.services.pokeapi import fetch_pokemon_range


def home(request):
    pokemons = fetch_pokemon_range(1, 151)
    return render(request, 'pokedex.html', {'pokemons': pokemons})
