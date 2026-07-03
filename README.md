# Pokédex Inteligente

Aplicação web visual construída com Django, HTML e CSS que exibe informações de diferentes Pokémons via **PokéAPI** e permite ao usuário interagir com uma **LLM via OpenRouter** para tirar dúvidas sobre o Pokémon selecionado.

![Página Home](/imgs/pokedex_home.png)

---

## Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Decisões Técnicas](#decisões-técnicas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Rodar Localmente](#como-rodar-localmente)
- [Variáveis de Ambiente](#variáveis-de-ambiente)

---

## Visão Geral

A Pokédex Inteligente é composta por duas páginas principais:

- **Pokédex (`/home/`)** — lista visual dos Pokémons com sprite, tipos e barras de atributos, consumindo dados em tempo real da PokéAPI.
- **Detalhe (`/pokemon/<id>/`)** — ficha completa do Pokémon selecionado, com uma área de consulta onde o usuário pode fazer perguntas a uma LLM e visualizar a resposta gerada pelo modelo.

![Página Analise](/imgs/Pokedex_analise.png)

---

## Funcionalidades

- Listagem de Pokémons com sprite, número, tipos e mini barras de HP e ATK
- Página de detalhe com ficha completa: altura, peso, habilidade, experiência base e barras de todos os stats
- Área de consulta com envio de perguntas para uma LLM via OpenRouter
- Exibição da resposta do modelo na mesma página
- Identidade visual inspirada na Pokédex clássica com estética de terminal CRT

---

## Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python 3.x | Linguagem principal |
| Django | Framework web (views, urls, templates, sessions) |
| HTML + CSS | Interface e identidade visual |
| PokéAPI | Fonte dos dados dos Pokémons |
| OpenRouter API | Acesso à LLM para responder perguntas |
| Python Requests | Requisições HTTP para as APIs externas |
| Django Sessions | Passagem de dados entre views via POST/redirect/GET |

---

## Decisões Técnicas

### Separação em apps Django
O projeto foi dividido em apps com responsabilidades distintas, seguindo a convenção Django de modularização. Cada app possui seu próprio `views.py` e `urls.py`, e o arquivo `urls.py` principal delega as rotas para cada app via `include()`.

### Consumo de API no servidor
As chamadas à PokéAPI e ao OpenRouter são feitas no servidor (nas views Django), não no navegador. Isso evita expor a chave da API do OpenRouter no frontend e centraliza o tratamento de erros.

### Padrão POST → Redirect → GET
O formulário de consulta ao modelo segue o padrão PRG (*Post/Redirect/Get*): o POST é processado pela view `pokemon_query`, que salva a resposta na session do Django e redireciona para `pokemon_detail` via GET. Isso evita o reenvio do formulário ao recarregar a página.

### Django Sessions para passagem de dados
A resposta da LLM é temporariamente armazenada na session do Django e consumida com `.pop()` na view de detalhe, garantindo que a resposta apareça apenas uma vez e seja limpa automaticamente após a exibição.

### Templates sem JavaScript externo
Toda a interface é construída com HTML e CSS puros, sem frameworks frontend. O único JavaScript presente é inline e mínimo: contador de caracteres no textarea e feedback visual no botão de envio.

---

## Estrutura do Projeto

```
pokedex_inteligente/
│
├── pokedex_inteligente/        # Configurações globais do projeto
│   ├── settings.py
│   ├── urls.py                 # Roteamento principal
│   └── wsgi.py
│
├── home/                       # App da lista (Pokédex)
│   ├── views.py                # View da listagem
│   ├── urls.py
│   └── templates/
│       └── pokedex.html
│
├── pokemon_detail/              # App de detalhe e consulta
│   ├── views.py                # Views pokemon_detail e pokemon_query
│   ├── urls.py
│   └── templates/
│       └── pokemon_detail.html

├── pokemon_detail/              # App de detalhe e consulta
│   ├── views.py                # Views pokemon_query
│   ├── urls.py
│   ├── openrouter.py           # Integração com a API do OpenRouter
│   
│
├── static/
│   └── css/
│       ├── pokedex.css
│       └── pokemon_detail.css
│
├── .env                        # Variáveis de ambiente (não versionar)
├── requirements.txt
└── manage.py
```

---

## Pré-requisitos

- Python 3.10 ou superior
- Git
- pip
- Conta e chave de API no [OpenRouter](https://openrouter.ai/)
- Conexão com internet (para consumo da PokéAPI e OpenRouter)

---

## Instalação e Configuração

**1. Clone o repositório**

```bash
git clone https://github.com/GMCavalheri/Desafio-Tecnico---Estagio-em-Engenharia-de-Software-levva
cd pokedex-inteligente
```

**2. Crie e ative um ambiente virtual**

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto (veja a seção [Variáveis de Ambiente](#variáveis-de-ambiente)).

**5. Execute as migrações**

```bash
python manage.py migrate
```

---

## Como Rodar Localmente

```bash
python manage.py runserver
```

Acesse no navegador: [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
SECRET_KEY=sua-secret-key-django-aqui
DEBUG=True
OPENROUTER_API_KEY=sua-chave-openrouter-aqui
```

> **Atenção:** nunca versione o arquivo `.env`. Adicione-o ao `.gitignore`.

Para gerar uma `SECRET_KEY` Django:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
