from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

SAMPLE_POKEMON = {
    'id': 25,
    'name': 'pikachu',
    'sprite_url': 'https://example.com/25.png',
    'types': ['electric'],
    'height_m': 0.4,
    'weight_kg': 6.0,
    'base_experience': 112,
    'ability': 'static',
    'stats': [],
    'hp_percent': 14,
    'atk_percent': 22,
}


class PokemonDetailViewTests(TestCase):
    @patch('pokemon_detail.views.fetch_pokemon')
    def test_renders_the_pokemon_profile(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_POKEMON

        response = self.client.get(reverse('pokemon_detail', args=[25]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pokemon_detail.html')
        self.assertContains(response, 'PIKACHU')
        mock_fetch.assert_called_once_with(25)

    @patch('pokemon_detail.views.fetch_pokemon')
    def test_ai_response_is_shown_once_then_cleared_from_the_session(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_POKEMON
        session = self.client.session
        session['ai_response'] = 'Pikachu is an Electric type.'
        session['last_question'] = 'What type is it?'
        session.save()

        first_visit = self.client.get(reverse('pokemon_detail', args=[25]))
        self.assertContains(first_visit, 'Pikachu is an Electric type.')

        second_visit = self.client.get(reverse('pokemon_detail', args=[25]))
        self.assertNotContains(second_visit, 'Pikachu is an Electric type.')

    @patch('pokemon_detail.views.fetch_pokemon')
    def test_shows_error_message_from_a_failed_query(self, mock_fetch):
        mock_fetch.return_value = SAMPLE_POKEMON
        session = self.client.session
        session['error_message'] = 'OpenRouter timed out.'
        session.save()

        response = self.client.get(reverse('pokemon_detail', args=[25]))

        self.assertContains(response, 'OpenRouter timed out.')
