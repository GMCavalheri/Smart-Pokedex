"""Thin client around PokéAPI, shared by the home and pokemon_detail apps.

Centralizing the fetch + parse logic here avoids duplicating it across
views and keeps a single place to add caching later.
"""
import requests

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"
MAX_STAT_VALUE = 255
REQUEST_TIMEOUT = 10


def _stat_percent(base_stat):
    return min(100, round(base_stat / MAX_STAT_VALUE * 100))


def _parse_pokemon(data):
    stats = [
        {
            'name': stat['stat']['name'],
            'value': stat['base_stat'],
            'percent': _stat_percent(stat['base_stat']),
        }
        for stat in data['stats']
    ]
    stats_by_name = {stat['name']: stat for stat in stats}

    return {
        'id': data['id'],
        'name': data['name'],
        'sprite_url': data['sprites']['front_default'],
        'types': [t['type']['name'] for t in data['types']],
        'height_m': data['height'] / 10,
        'weight_kg': data['weight'] / 10,
        'base_experience': data['base_experience'],
        'ability': data['abilities'][0]['ability']['name'] if data['abilities'] else None,
        'stats': stats,
        'hp_percent': stats_by_name.get('hp', {}).get('percent', 0),
        'atk_percent': stats_by_name.get('attack', {}).get('percent', 0),
    }


def fetch_pokemon(pokemon_id_or_name):
    """Fetch and parse a single Pokémon by numeric id or name."""
    response = requests.get(
        f'{POKEAPI_BASE_URL}/{str(pokemon_id_or_name).lower()}',
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return _parse_pokemon(response.json())


def fetch_pokemon_range(start=1, end=151):
    """Fetch and parse Pokémon with ids in the inclusive [start, end] range."""
    return [fetch_pokemon(pokemon_id) for pokemon_id in range(start, end + 1)]
