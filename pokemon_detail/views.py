from django.shortcuts import render
import json
import requests

# Create your views here.

def pokemon_detail(request, pokemon_id):
    # Busca da PokéAPI
    data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()

    stats = []
    for s in data['stats']:
        stats.append({
            'name': s['stat']['name'],       # ex: "special-attack"
            'value': s['base_stat'],
            'percent': min(100, round(s['base_stat'] / 255 * 100))
        })

    pokemon = {
        'id': data['id'],
        'name': data['name'],
        'sprite_url': data['sprites']['front_default'],
        'types': [t['type']['name'] for t in data['types']],
        'height_m': data['height'] / 10,
        'weight_kg': data['weight'] / 10,
        'base_experience': data['base_experience'],
        'ability': data['abilities'][0]['ability']['name'],
        'stats': stats,
    }

    # Lê e limpa a session (para não persistir entre visitas)
    ai_response   = request.session.pop('ai_response', None)
    error_message = request.session.pop('error_message', None)
    last_question = request.session.pop('last_question', '')

    context = {
        'pokemon': pokemon,
        'question': last_question,
        'ai_response': ai_response,
        'model_name': 'openrouter/free',
        'error_message': error_message,
    }
    return render(request, 'pokemon_detail.html', context)