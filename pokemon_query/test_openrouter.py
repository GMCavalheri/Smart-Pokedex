from unittest.mock import Mock, patch

from django.test import SimpleTestCase, override_settings

from pokemon_query import openrouter


class BuildPromptTests(SimpleTestCase):
    def test_includes_question_and_pokemon_name(self):
        prompt = openrouter.build_prompt('How strong is it?', 'pikachu')

        self.assertIn('pikachu', prompt)
        self.assertIn('How strong is it?', prompt)


class AskTests(SimpleTestCase):
    @override_settings(OPENROUTER_API_KEY='test-key')
    @patch('pokemon_query.openrouter.requests.post')
    def test_sends_expected_request_and_returns_answer(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Pikachu is an Electric type.'}}]
        }
        mock_post.return_value = mock_response

        answer = openrouter.ask(question='What type is it?', pokemon_name='pikachu')

        self.assertEqual(answer, 'Pikachu is an Electric type.')

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test-key')
        self.assertIn('pikachu', kwargs['json']['messages'][0]['content'])

    @override_settings(OPENROUTER_API_KEY='test-key')
    @patch('pokemon_query.openrouter.requests.post')
    def test_raises_when_the_api_returns_an_error_status(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception('502 Bad Gateway')
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            openrouter.ask(question='What type is it?', pokemon_name='pikachu')
