from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class PokemonQueryViewTests(TestCase):
    def test_get_redirects_to_detail_without_calling_openrouter(self):
        with patch('pokemon_query.openrouter.ask') as mock_ask:
            response = self.client.get(reverse('pokemon_query', args=[25]))

        mock_ask.assert_not_called()
        self.assertRedirects(
            response, reverse('pokemon_detail', args=[25]), fetch_redirect_response=False
        )

    def test_blank_question_redirects_without_calling_openrouter(self):
        with patch('pokemon_query.openrouter.ask') as mock_ask:
            response = self.client.post(
                reverse('pokemon_query', args=[25]),
                {'question': '   ', 'pokemon_name': 'pikachu'},
            )

        mock_ask.assert_not_called()
        self.assertRedirects(
            response, reverse('pokemon_detail', args=[25]), fetch_redirect_response=False
        )

    @patch('pokemon_query.openrouter.ask')
    def test_valid_question_stores_the_answer_in_the_session(self, mock_ask):
        mock_ask.return_value = 'Pikachu is an Electric type.'

        response = self.client.post(
            reverse('pokemon_query', args=[25]),
            {'question': 'What type is it?', 'pokemon_name': 'pikachu'},
        )

        self.assertRedirects(
            response, reverse('pokemon_detail', args=[25]), fetch_redirect_response=False
        )
        session = self.client.session
        self.assertEqual(session['ai_response'], 'Pikachu is an Electric type.')
        self.assertIsNone(session['error_message'])
        mock_ask.assert_called_once_with(question='What type is it?', pokemon_name='pikachu')

    @patch('pokemon_query.openrouter.ask')
    def test_openrouter_failure_stores_an_error_message_instead(self, mock_ask):
        mock_ask.side_effect = Exception('OpenRouter timed out.')

        response = self.client.post(
            reverse('pokemon_query', args=[25]),
            {'question': 'What type is it?', 'pokemon_name': 'pikachu'},
        )

        self.assertRedirects(
            response, reverse('pokemon_detail', args=[25]), fetch_redirect_response=False
        )
        session = self.client.session
        self.assertIsNone(session['ai_response'])
        self.assertEqual(session['error_message'], 'OpenRouter timed out.')
