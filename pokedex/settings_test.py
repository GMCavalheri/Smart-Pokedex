"""Settings used only when running the test suite.

Tests don't need a real MySQL/Redis server: this app has no MySQL-specific
SQL and nothing that depends on Redis's actual behavior, so swapping in
SQLite (in-memory) and Django's local-memory cache keeps the suite fast and
runnable with zero external services — no Docker required.
"""
from .settings import *  # noqa: F401,F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
