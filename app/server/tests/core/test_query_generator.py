import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_random_query_with_openai,
    generate_random_query_with_anthropic,
    generate_random_query
)


class TestQueryGenerator:

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_success(self, mock_openai_class):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "What is the average price of products?"
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_random_query_with_openai(schema_info)

            assert result == "What is the average price of products?"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.9  # High temp for variety
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_removes_quotes(self, mock_openai_class):
        # Test query cleanup - remove surrounding quotes
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '"Show me all users from last month"'
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 100
                    }
                }
            }

            result = generate_random_query_with_openai(schema_info)

            assert result == "Show me all users from last month"

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_multiple_tables(self, mock_openai_class):
        # Test with multiple tables
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Count the orders per user"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 100
                    },
                    'orders': {
                        'columns': {'id': 'INTEGER', 'user_id': 'INTEGER', 'total': 'REAL'},
                        'row_count': 250
                    }
                }
            }

            result = generate_random_query_with_openai(schema_info)

            assert result == "Count the orders per user"

    def test_generate_random_query_with_openai_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_openai(schema_info)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_api_error(self, mock_openai_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_openai(schema_info)

            assert "Error generating query with OpenAI" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_random_query_with_anthropic_success(self, mock_anthropic_class):
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Find the top 5 most expensive items"
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'items': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 200
                    }
                }
            }

            result = generate_random_query_with_anthropic(schema_info)

            assert result == "Find the top 5 most expensive items"
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.9
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.Anthropic')
    def test_generate_random_query_with_anthropic_removes_quotes(self, mock_anthropic_class):
        # Test query cleanup - remove surrounding quotes
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "'Show me all records'"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'records': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 50
                    }
                }
            }

            result = generate_random_query_with_anthropic(schema_info)

            assert result == "Show me all records"

    def test_generate_random_query_with_anthropic_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_anthropic(schema_info)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_random_query_with_anthropic_api_error(self, mock_anthropic_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 0}}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_anthropic(schema_info)

            assert "Error generating query with Anthropic" in str(exc_info.value)

    @patch('core.llm_processor.generate_random_query_with_openai')
    def test_generate_random_query_openai_priority(self, mock_openai_func):
        # Test that OpenAI is used when OpenAI key exists
        mock_openai_func.return_value = "What is the total count of users?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_random_query(schema_info)

            assert result == "What is the total count of users?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_random_query_with_anthropic')
    def test_generate_random_query_anthropic_fallback(self, mock_anthropic_func):
        # Test that Anthropic is used when only Anthropic key exists
        mock_anthropic_func.return_value = "Show me products by category"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'category': 'TEXT'},
                        'row_count': 50
                    }
                }
            }

            result = generate_random_query(schema_info)

            assert result == "Show me products by category"
            mock_anthropic_func.assert_called_once_with(schema_info)

    def test_generate_random_query_no_api_keys(self):
        # Test error when no API keys are configured
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            with pytest.raises(ValueError) as exc_info:
                generate_random_query(schema_info)

            assert "No LLM API keys configured" in str(exc_info.value)

    def test_generate_random_query_empty_database(self):
        # Test error when database has no tables
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(ValueError) as exc_info:
                generate_random_query(schema_info)

            assert "No tables available in database" in str(exc_info.value)

    def test_generate_random_query_no_tables_key(self):
        # Test error when schema_info doesn't have tables key
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {}

            with pytest.raises(ValueError) as exc_info:
                generate_random_query(schema_info)

            assert "No tables available in database" in str(exc_info.value)

    @patch('core.llm_processor.generate_random_query_with_openai')
    def test_generate_random_query_single_table(self, mock_openai_func):
        # Test with single table
        mock_openai_func.return_value = "Count all records in the table"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'records': {
                        'columns': {'id': 'INTEGER', 'value': 'TEXT'},
                        'row_count': 10
                    }
                }
            }

            result = generate_random_query(schema_info)

            assert result == "Count all records in the table"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_random_query_with_openai')
    def test_generate_random_query_table_with_zero_rows(self, mock_openai_func):
        # Test with table that has zero rows (edge case)
        mock_openai_func.return_value = "Show me all entries"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'entries': {
                        'columns': {'id': 'INTEGER'},
                        'row_count': 0
                    }
                }
            }

            result = generate_random_query(schema_info)

            assert result == "Show me all entries"
            mock_openai_func.assert_called_once_with(schema_info)
