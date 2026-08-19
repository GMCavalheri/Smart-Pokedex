import requests
from django.conf import settings

MODEL = "openrouter/free"


def build_prompt(question, pokemon_name):
    """Build the prompt that steers the LLM's persona and answer style."""
    return f"""You are a Pokémon expert whose job is to answer a user's questions on this topic.
Your answers should be simple, educational and patient, as if explaining to a child.

Answer about {pokemon_name}: {question}
"""


def ask(question: str, pokemon_name: str) -> str:
    prompt = build_prompt(question, pokemon_name)

    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': MODEL,
            'messages': [{'role': 'user', 'content': prompt}],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']
