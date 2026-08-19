from unittest.mock import Mock, patch

from django.core.cache import cache
from django.test import SimpleTestCase

from pokedex.services import pokeapi

RAW_PIKACHU = {
    'id': 25,
    'name': 'pikachu',
    'sprites': {'front_default': 'https://example.com/25.png'},
    'types': [{'type': {'name': 'electric'}}],
    'height': 4,
    'weight': 60,
    'base_experience': 112,
    'abilities': [{'ability': {'name': 'static'}}],
    'stats': [
        {'stat': {'name': 'hp'}, 'base_stat': 35},
        {'stat': {'name': 'attack'}, 'base_stat': 55},
    ],
}


def _mock_response(json_data):
    response = Mock()
    response.json.return_value = json_data
    response.raise_for_status.return_value = None
    return response


class StatPercentTests(SimpleTestCase):
    def test_caps_at_100(self):
        self.assertEqual(pokeapi._stat_percent(255), 100)
        self.assertEqual(pokeapi._stat_percent(300), 100)

    def test_rounds_normally(self):
        self.assertEqual(pokeapi._stat_percent(0), 0)
        self.assertEqual(pokeapi._stat_percent(128), 50)


class ParsePokemonTests(SimpleTestCase):
    def test_extracts_expected_fields(self):
        parsed = pokeapi._parse_pokemon(RAW_PIKACHU)

        self.assertEqual(parsed['id'], 25)
        self.assertEqual(parsed['name'], 'pikachu')
        self.assertEqual(parsed['types'], ['electric'])
        self.assertEqual(parsed['height_m'], 0.4)
        self.assertEqual(parsed['weight_kg'], 6.0)
        self.assertEqual(parsed['ability'], 'static')
        self.assertEqual(parsed['hp_percent'], pokeapi._stat_percent(35))
        self.assertEqual(parsed['atk_percent'], pokeapi._stat_percent(55))

    def test_handles_no_abilities(self):
        data = {**RAW_PIKACHU, 'abilities': []}
        parsed = pokeapi._parse_pokemon(data)
        self.assertIsNone(parsed['ability'])


class FetchPokemonTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    @patch('pokedex.services.pokeapi.requests.get')
    def test_fetches_and_parses(self, mock_get):
        mock_get.return_value = _mock_response(RAW_PIKACHU)

        pokemon = pokeapi.fetch_pokemon(25)

        mock_get.assert_called_once_with(
            f'{pokeapi.POKEAPI_BASE_URL}/25', timeout=pokeapi.REQUEST_TIMEOUT
        )
        self.assertEqual(pokemon['name'], 'pikachu')

    @patch('pokedex.services.pokeapi.requests.get')
    def test_second_call_is_served_from_cache(self, mock_get):
        mock_get.return_value = _mock_response(RAW_PIKACHU)

        pokeapi.fetch_pokemon(25)
        pokeapi.fetch_pokemon(25)

        mock_get.assert_called_once()

    @patch('pokedex.services.pokeapi.requests.get')
    def test_cache_key_is_case_insensitive(self, mock_get):
        mock_get.return_value = _mock_response(RAW_PIKACHU)

        pokeapi.fetch_pokemon('Pikachu')
        pokeapi.fetch_pokemon('pikachu')

        mock_get.assert_called_once()


class FetchPokemonRangeTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    @patch('pokedex.services.pokeapi.requests.get')
    def test_fetches_each_id_in_the_inclusive_range(self, mock_get):
        mock_get.return_value = _mock_response(RAW_PIKACHU)

        result = pokeapi.fetch_pokemon_range(1, 3)

        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(len(result), 3)
