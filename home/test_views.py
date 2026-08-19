from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

SAMPLE_POKEMON = {
    'id': 1,
    'name': 'bulbasaur',
    'sprite_url': 'https://example.com/1.png',
    'types': ['grass', 'poison'],
    'hp_percent': 18,
    'atk_percent': 19,
}


class HomeViewTests(TestCase):
    @patch('home.views.fetch_pokemon_range')
    def test_renders_the_pokemon_list(self, mock_fetch_range):
        mock_fetch_range.return_value = [SAMPLE_POKEMON]

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokedex.html')
        self.assertContains(response, 'bulbasaur')
        mock_fetch_range.assert_called_once_with(1, 151)

    @patch('home.views.fetch_pokemon_range')
    def test_renders_the_empty_state_when_the_api_returns_nothing(self, mock_fetch_range):
        mock_fetch_range.return_value = []

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Pokémon found')
