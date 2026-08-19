from django.shortcuts import render

from pokedex.services.pokeapi import fetch_pokemon


def pokemon_detail(request, pokemon_id):
    pokemon = fetch_pokemon(pokemon_id)

    # Read and clear the session so the AI answer doesn't persist across visits.
    ai_response = request.session.pop('ai_response', None)
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
