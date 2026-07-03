import requests

OPENROUTER_API_KEY = "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"
MODEL = "openrouter/free"

def intrucoes_modelo(question, pokemon_name):
  
  # Definindo o prompt anterior ao usuário, para direcionar o modelo na forma de reponder o usuário

  intrucoes = f"""Você é um especialista em pokémons e seu papel é respoder dúvidas de um usuário sobre esse tema.
                  Suas respostas devem ser simples, didáticas e com paciência, como se o usuário fosse uma criança.

                  Responda sobre {pokemon_name}: {question}   
                  """

  return intrucoes

def ask(question: str, pokemon_name: str) -> str:

    prompt = intrucoes_modelo(question, pokemon_name)
    
    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type':  'application/json',
        },
        json={
            'model':    MODEL,
            'messages': [{'role': 'user', 'content': prompt}],
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']