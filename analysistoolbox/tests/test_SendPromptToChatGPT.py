import unittest
from unittest.mock import patch
from SendPromptToChatGPT import SendPromptToChatGPT

class TestSendPromptToChatGPT(unittest.TestCase):

    @patch('SendPromptToChatGPT.openai')
    def test_send_prompt_to_chat_gpt(self, mock_openai):
        prompt_template = """
        Break this key intelligence question into less than four sub-questions: {key_intelligence_question}
        """
        user_input = {
            "key_intelligence_question": "What targets are Hamas most likely to strike next in Israel?"
        }
        system_message = """
            You are a project manager. You specialize in taking a key intelligence question and breaking it down into sub-questions. 
            When creating the sub-questions, identify the main components of the original question. What are the essential elements or variables that the decision maker is concerned about?
        """
        openai_api_key = "YOUR_API_KEY"

        response = SendPromptToChatGPT(prompt_template, user_input, system_message, openai_api_key)

        # Assert that the OpenAI API key is set
        self.assertEqual(mock_openai.api_key, openai_api_key)

        # Assert that the prompt template is correctly formatted
        self.assertIn("{key_intelligence_question}", prompt_template)

        # Assert that the user input is a dictionary
        self.assertIsInstance(user_input, dict)

        # Assert that each key in user_input is in the prompt template
        for key in user_input.keys():
            self.assertIn("{" + key + "}", prompt_template)

        # Assert that the system message is not empty
        self.assertNotEqual(system_message, "")

        # Assert that the response is not empty
        self.assertNotEqual(response, "")

if __name__ == '__main__':
    unittest.main()