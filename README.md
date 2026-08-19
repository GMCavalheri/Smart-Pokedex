# Smart Pokédex

A visual web application built with Django, HTML and CSS that displays Pokémon information via the **PokéAPI** and lets the user interact with an **LLM through OpenRouter** to ask questions about the selected Pokémon.

![Home page](/imgs/pokedex_home.png)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Technical Decisions](#technical-decisions)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running Locally](#running-locally)
- [Environment Variables](#environment-variables)

---

## Overview

The Smart Pokédex is made up of two main pages:

- **Pokédex (`/home/`)** — a visual list of Pokémon with sprite, types and attribute bars, consuming real-time data from the PokéAPI.
- **Detail (`/pokemon/<id>/`)** — a full profile of the selected Pokémon, with a query area where the user can ask an LLM questions and see the model's generated answer.

![Analysis page](/imgs/Pokedex_analise.png)

---

## Features

- List of Pokémon with sprite, number, types and mini HP/ATK bars
- Detail page with a full profile: height, weight, ability, base experience and bars for every stat
- Query area to send questions to an LLM via OpenRouter
- The model's answer is displayed on the same page
- Visual identity inspired by the classic Pokédex, with a CRT terminal aesthetic

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.x | Main language |
| Django | Web framework (views, urls, templates, sessions) |
| HTML + CSS | Interface and visual identity |
| PokéAPI | Source of Pokémon data |
| OpenRouter API | Access to the LLM that answers questions |
| Python Requests | HTTP requests to the external APIs |
| Django Sessions | Passing data between views via POST/redirect/GET |
| MySQL | Relational database (via PyMySQL) |

---

## Technical Decisions

### Split into Django apps
The project is split into apps with distinct responsibilities, following Django's modularization convention. Each app has its own `views.py` and `urls.py`, and the main `urls.py` delegates routes to each app via `include()`.

### Shared PokéAPI service layer
Fetching and parsing PokéAPI data lives in a single module (`pokedex/services/pokeapi.py`), reused by both the `home` and `pokemon_detail` apps, instead of being duplicated per view.

### API calls happen on the server
Calls to the PokéAPI and OpenRouter are made server-side (in Django views), not in the browser. This avoids exposing the OpenRouter API key on the frontend and centralizes error handling.

### POST → Redirect → GET pattern
The model query form follows the PRG pattern (*Post/Redirect/Get*): the POST is handled by the `pokemon_query` view, which saves the answer in the Django session and redirects to `pokemon_detail` via GET. This avoids resubmitting the form on page reload.

### Django Sessions for passing data
The LLM's answer is temporarily stored in the Django session and consumed with `.pop()` in the detail view, guaranteeing it's shown only once and cleared automatically afterwards.

### Templates without external JavaScript
The whole interface is built with plain HTML and CSS, with no frontend framework. The only JavaScript present is inline and minimal: a character counter for the textarea and visual feedback on the submit button.

### Configuration via environment variables
Secrets (Django `SECRET_KEY`, `OPENROUTER_API_KEY`) and environment-dependent settings (`DEBUG`, `ALLOWED_HOSTS`, database credentials) are read from a local `.env` file via `python-dotenv`, never hardcoded in source.

### MySQL via PyMySQL
The project uses MySQL as its relational database, connected through `PyMySQL` — a pure-Python driver. Unlike `mysqlclient` (the more common choice), it needs no native build tools to install, so it works the same way on every OS and inside Docker without extra system packages. Database connection settings (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`) come from the `.env` file.

---

## Project Structure

```
pokedex/
│
├── pokedex/                    # Global project configuration
│   ├── settings.py
│   ├── urls.py                 # Main routing
│   ├── wsgi.py / asgi.py
│   └── services/
│       └── pokeapi.py          # Shared PokéAPI client
│
├── home/                       # Pokédex list app
│   ├── views.py
│   └── templates/
│       └── pokedex.html
│
├── pokemon_detail/             # Detail app
│   ├── views.py
│   └── templates/
│       └── pokemon_detail.html
│
├── pokemon_query/              # LLM query app
│   ├── views.py
│   └── openrouter.py           # OpenRouter API integration
│
├── templates/
│   └── static/
│       └── css/
│           ├── pokedex.css
│           └── pokemon_detail.css
│
├── .env                        # Environment variables (not versioned)
├── .env.example                # Template for .env
├── requirements.txt
└── manage.py
```

---

## Prerequisites

- Python 3.10 or higher
- Git
- pip
- A running MySQL server (a `docker-compose` setup for this is coming in a later step)
- An account and API key from [OpenRouter](https://openrouter.ai/)
- Internet connection (to consume the PokéAPI and OpenRouter)

---

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/GMCavalheri/Desafio-Tecnico---Estagio-em-Engenharia-de-Software-levva pokedex-inteligente
cd pokedex-inteligente
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root (see the [Environment Variables](#environment-variables) section). Make sure `DB_*` points to a running MySQL server with a matching database and user already created.

**5. Run migrations**

```bash
python manage.py migrate
```

---

## Running Locally

```bash
python manage.py runserver
```

Open in your browser: [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your own values:

```bash
cp .env.example .env
```

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
OPENROUTER_API_KEY=your-openrouter-api-key-here

# MySQL
DB_NAME=pokedex
DB_USER=pokedex_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=3306
```

> **Warning:** never commit the `.env` file. It is already listed in `.gitignore`.

To generate a Django `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
