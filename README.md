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
- [Running with Docker](#running-with-docker)
- [Installation and Setup (without Docker)](#installation-and-setup-without-docker)
- [Running Locally (without Docker)](#running-locally-without-docker)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)

---

## Overview

The Smart Pokédex is made up of two main pages:

- **Pokédex (`/home/`)** — a visual list of Pokémon with sprite, types and attribute bars, consuming real-time data from the PokéAPI.
- **Detail (`/pokemon/<id>/`)** — a full profile of the selected Pokémon, with a query area where the user can ask an LLM questions and see the model's generated answer.

![Analysis page](/imgs/pokedex_analise.png)

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
| Redis | Caching layer for PokéAPI responses |
| Docker + Docker Compose | Containerized app, database and cache for a one-command setup |
| pytest + pytest-django | Automated test suite |

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

### Redis cache for PokéAPI responses
The home page originally fetched all 151 Pokémon from the PokéAPI sequentially, one HTTP request at a time, on every single page load — around 18 seconds per load in testing. `pokedex/services/pokeapi.py` now checks Redis (via Django's built-in cache framework, `django.core.cache.backends.redis.RedisCache`) before making a request, and caches the parsed result for 24 hours (a Pokémon's base stats/types/sprite essentially never change). After the first load, subsequent loads read entirely from Redis — down to tens of milliseconds. Redis connection settings (`REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`) come from the `.env` file.

### Containerized with Docker Compose
Three services run together: `web` (this Django app), `db` (MySQL) and `redis` (Redis). `db` and `redis` don't publish ports to the host — only `web` does — since only `web` needs to reach them, and this avoids clashing with any MySQL/Redis you may already have running locally. `web` waits for `db` and `redis` to report healthy (via Compose's `depends_on: condition: service_healthy`) before starting, and `entrypoint.sh` runs `manage.py migrate` automatically on every container start, so the schema is always up to date. Host/port values for `DB_HOST`/`REDIS_HOST` are overridden directly in `docker-compose.yml` (to the service names `db`/`redis`) rather than taken from `.env`, since `.env`'s `127.0.0.1` only makes sense for running the app outside Docker.

### Tests run against SQLite and a local-memory cache, not the real services
`pokedex/settings_test.py` swaps `DATABASES` to an in-memory SQLite database and `CACHES` to Django's `LocMemCache`, used only when running `pytest` (wired up in `pytest.ini`). Since the app has no MySQL-specific SQL and nothing that depends on Redis's actual behavior, this keeps the test suite fast and independent of Docker/MySQL/Redis being up — important both for a quick local feedback loop and for CI. Every PokéAPI and OpenRouter call is mocked (`unittest.mock.patch`) rather than hitting the real network, so tests can't fail because of an outage or rate limit on either external service.

---

## Project Structure

```
pokedex/
│
├── pokedex/                    # Global project configuration
│   ├── settings.py
│   ├── settings_test.py        # Settings used only by pytest (SQLite + local-memory cache)
│   ├── urls.py                 # Main routing
│   ├── wsgi.py / asgi.py
│   └── services/
│       ├── pokeapi.py          # Shared PokéAPI client
│       └── test_pokeapi.py
│
├── home/                       # Pokédex list app
│   ├── views.py
│   ├── test_views.py
│   └── templates/
│       └── pokedex.html
│
├── pokemon_detail/             # Detail app
│   ├── views.py
│   ├── test_views.py
│   └── templates/
│       └── pokemon_detail.html
│
├── pokemon_query/              # LLM query app
│   ├── views.py
│   ├── test_views.py
│   ├── openrouter.py           # OpenRouter API integration
│   └── test_openrouter.py
│
├── templates/
│   └── static/
│       └── css/
│           ├── pokedex.css
│           └── pokemon_detail.css
│
├── .env                    # Environment variables (not versioned)
├── .env.example            # Template for .env
├── Dockerfile              # Image for the web service
├── entrypoint.sh           # Runs migrations, then starts the app
├── docker-compose.yml      # Wires up web + MySQL + Redis
├── pytest.ini              # pytest / pytest-django configuration
├── requirements.txt
├── requirements-dev.txt    # requirements.txt + pytest tooling
└── manage.py
```

---

## Prerequisites

- Git
- An account and API key from [OpenRouter](https://openrouter.ai/)
- Internet connection (to consume the PokéAPI and OpenRouter)
- **To run with Docker (recommended):** Docker and Docker Compose
- **To run without Docker:** Python 3.10+, pip, a running MySQL server and a running Redis server

---

## Running with Docker

This is the fastest way to get everything running — Django, MySQL and Redis — with a single command, no local Python or database setup required.

**1. Clone the repository**

```bash
git clone https://github.com/GMCavalheri/Desafio-Tecnico---Estagio-em-Engenharia-de-Software-levva pokedex-inteligente
cd pokedex-inteligente
```

**2. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in `SECRET_KEY`, `OPENROUTER_API_KEY`, and set your own `DB_PASSWORD`/`DB_ROOT_PASSWORD` (see [Environment Variables](#environment-variables)). You can leave `DB_HOST`/`REDIS_HOST` as-is — `docker-compose.yml` overrides them automatically for the containers.

**3. Build and start everything**

```bash
docker compose up --build
```

This builds the app image, starts `db` (MySQL) and `redis`, waits for both to be healthy, then starts `web` — which runs migrations automatically before serving.

Open in your browser: [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

**4. Stop everything**

```bash
docker compose down
```

Add `-v` (`docker compose down -v`) if you also want to wipe the MySQL data volume.

**Made a code change?** Rebuild the image so it's picked up:

```bash
docker compose up --build
```

---

## Installation and Setup (without Docker)

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

Create a `.env` file in the project root (see the [Environment Variables](#environment-variables) section). Make sure `DB_*` points to a running MySQL server with a matching database and user already created, and `REDIS_*` points to a running Redis server.

**5. Run migrations**

```bash
python manage.py migrate
```

---

## Running Locally (without Docker)

```bash
python manage.py runserver
```

Open in your browser: [http://127.0.0.1:8000/home/](http://127.0.0.1:8000/home/)

---

## Running Tests

The test suite uses `pytest` + `pytest-django`, and needs no external services — no MySQL, no Redis, no Docker. Tests run against an in-memory SQLite database and Django's local-memory cache instead (`pokedex/settings_test.py`), and every call to the PokéAPI or OpenRouter is mocked, so the suite is fast and fully offline.

**1. Install the dev dependencies** (adds `pytest`, `pytest-django` and `pytest-cov` on top of `requirements.txt`)

```bash
pip install -r requirements-dev.txt
```

**2. Run the suite**

```bash
pytest
```

**3. (Optional) Run with a coverage report**

```bash
pytest --cov=home --cov=pokemon_detail --cov=pokemon_query --cov=pokedex/services --cov-report=term-missing
```

Test files live next to the code they cover, named `test_*.py`:

- `pokedex/services/test_pokeapi.py` — parsing logic, stat percentage math, and that a second call for the same Pokémon is served from cache instead of hitting the network again.
- `pokemon_query/test_openrouter.py` — prompt building and the OpenRouter request/response handling.
- `home/test_views.py`, `pokemon_detail/test_views.py`, `pokemon_query/test_views.py` — each view's behavior through Django's test client, including the session-based POST → Redirect → GET flow and its error path.

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
DB_ROOT_PASSWORD=your-db-root-password
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

> **Warning:** never commit the `.env` file. It is already listed in `.gitignore`.

> **Note:** `DB_ROOT_PASSWORD` is only used by the MySQL container itself (its root superuser account, set up in `docker-compose.yml`) — Django never uses it. `DB_HOST`/`DB_PORT`/`REDIS_HOST`/`REDIS_PORT` here are for running the app *without* Docker; when running via `docker compose`, those four are overridden automatically (see [Running with Docker](#running-with-docker)).

To generate a Django `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
