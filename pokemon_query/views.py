from django.shortcuts import redirect

from . import openrouter


def pokemon_query(request, pokemon_id):
    if request.method != 'POST':
        return redirect('pokemon_detail', pokemon_id=pokemon_id)

    question = request.POST.get('question', '').strip()
    pokemon_name = request.POST.get('pokemon_name', '')

    if not question:
        return redirect('pokemon_detail', pokemon_id=pokemon_id)

    try:
        ai_response = openrouter.ask(question=question, pokemon_name=pokemon_name)
        request.session['ai_response'] = ai_response
        request.session['error_message'] = None
    except Exception as e:
        request.session['ai_response'] = None
        request.session['error_message'] = str(e)

    request.session['last_question'] = question

    return redirect('pokemon_detail', pokemon_id=pokemon_id)
