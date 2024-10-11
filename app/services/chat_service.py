"""
Chat service module for handling chat model operations.

This module provides services for interacting with various chat models
and performing cost calculations.
"""

from config import settings
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatPerplexity
from langchain_together import ChatTogether
from langchain.chains import LLMChain
import tiktoken
from anthropic import Anthropic
from vertexai.preview import tokenization


class ChatService:
    """Service for chat-related operations."""

    def __init__(self):
        """Initialize the ChatService with model configurations."""
        self.model_company_mapping = {
            "gpt-3.5-turbo": {
                "model": ChatOpenAI,
                "premium": False,
                "company": "OpenAI",
                "input_token_cost_per_million": 0.5,
                "output_token_cost_per_million": 1.5,
            },
            "gpt-4-turbo-preview": {
                "model": ChatOpenAI,
                "premium": True,
                "company": "OpenAI",
                "input_token_cost_per_million": 10.0,
                "output_token_cost_per_million": 30.0,
            },
            "gpt-4o-mini": {
                "model": ChatOpenAI,
                "premium": False,
                "company": "OpenAI",
                "input_token_cost_per_million": 0.15,
                "output_token_cost_per_million": 0.6,
            },
            "gpt-4o": {
                "model": ChatOpenAI,
                "premium": True,
                "company": "OpenAI",
                "input_token_cost_per_million": 5.0,
                "output_token_cost_per_million": 15.0,
            },
            "claude-3-opus-20240229": {
                "model": ChatAnthropic,
                "premium": True,
                "company": "Anthropic",
                "input_token_cost_per_million": 15.0,
                "output_token_cost_per_million": 75.0,
            },
            "claude-3-sonnet-20240229": {
                "model": ChatAnthropic,
                "premium": True,
                "company": "Anthropic",
                "input_token_cost_per_million": 3.0,
                "output_token_cost_per_million": 15.0,
            },
            "claude-3-haiku-20240307": {
                "model": ChatAnthropic,
                "premium": False,
                "company": "Anthropic",
                "input_token_cost_per_million": 0.25,
                "output_token_cost_per_million": 1.25,
            },
            "claude-3-5-sonnet-20240620": {
                "model": ChatAnthropic,
                "premium": True,
                "company": "Anthropic",
                "input_token_cost_per_million": 3.0,
                "output_token_cost_per_million": 15.0,
            },
            "mistral-tiny-2312": {
                "model": ChatMistralAI,
                "premium": False,
                "company": "Mistral",
                "input_token_cost_per_million": 0.25,
                "output_token_cost_per_million": 0.25,
            },
            "mistral-small-2312": {
                "model": ChatMistralAI,
                "premium": False,
                "company": "Mistral",
                "input_token_cost_per_million": 0.7,
                "output_token_cost_per_million": 0.7,
            },
            "mistral-small-2402": {
                "model": ChatMistralAI,
                "premium": False,
                "company": "Mistral",
                "input_token_cost_per_million": 1.0,
                "output_token_cost_per_million": 3.0,
            },
            "mistral-medium-2312": {
                "model": ChatMistralAI,
                "premium": True,
                "company": "Mistral",
                "input_token_cost_per_million": 2.7,
                "output_token_cost_per_million": 8.1,
            },
            "mistral-large-2402": {
                "model": ChatMistralAI,
                "premium": True,
                "company": "Mistral",
                "input_token_cost_per_million": 4.0,
                "output_token_cost_per_million": 12.0,
            },
            "gemini-1.0-pro": {
                "model": ChatGoogleGenerativeAI,
                "premium": False,
                "company": "Google",
                "input_token_cost_per_million": 0.5,
                "output_token_cost_per_million": 1.5,
            },
            "gemini-1.5-flash-latest": {
                "model": ChatGoogleGenerativeAI,
                "premium": False,
                "company": "Google",
                "input_token_cost_per_million": 0.35,
                "output_token_cost_per_million": 1.05,
            },
            "gemini-1.5-pro-latest": {
                "model": ChatGoogleGenerativeAI,
                "premium": True,
                "company": "Google",
                "input_token_cost_per_million": 3.5,
                "output_token_cost_per_million": 10.5,
            },
            "llama-3-sonar-small-32k-online": {
                "model": ChatPerplexity,
                "premium": False,
                "company": "Perplexity",
                "input_token_cost_per_million": 0.2,
                "output_token_cost_per_million": 0.2,
            },
            "llama-3-sonar-small-32k-chat": {
                "model": ChatPerplexity,
                "premium": True,
                "company": "Perplexity",
                "input_token_cost_per_million": 0.2,
                "output_token_cost_per_million": 0.2,
            },
            "llama-3-sonar-large-32k-online": {
                "model": ChatPerplexity,
                "premium": False,
                "company": "Perplexity",
                "input_token_cost_per_million": 1,
                "output_token_cost_per_million": 1,
            },
            "llama-3-sonar-large-32k-chat": {
                "model": ChatPerplexity,
                "premium": True,
                "company": "Perplexity",
                "input_token_cost_per_million": 1,
                "output_token_cost_per_million": 1,
            },
            "llama-3.1-sonar-small-128k-online": {
                "model": ChatPerplexity,
                "premium": True,
                "company": "Perplexity",
                "input_token_cost_per_million": 0.2,
                "output_token_cost_per_million": 0.2,
            },
            "llama-3.1-sonar-small-128k-chat": {
                "model": ChatPerplexity,
                "premium": True,
                "company": "Perplexity",
                "input_token_cost_per_million": 0.2,
                "output_token_cost_per_million": 0.2,
            },
            "llama-3.1-sonar-large-128k-online": {
                "model": ChatPerplexity,
                "premium": True,
                "company": "Perplexity",
                "input_token_cost_per_million": 1,
                "output_token_cost_per_million": 1,
            },
            "llama-3.1-sonar-large-128k-chat": {
                "model": ChatPerplexity,
                "premium": True,
                "company": "Perplexity",
                "input_token_cost_per_million": 1,
                "output_token_cost_per_million": 1,
            },
            "codellama/CodeLlama-34b-Instruct-hf": {
                "model": ChatTogether,
                "premium": False,
                "company": "Meta",
                "input_token_cost_per_million": 0.78,
                "output_token_cost_per_million": 0.78,
            },
            "codellama/CodeLlama-70b-Instruct-hf": {
                "model": ChatTogether,
                "premium": True,
                "company": "Meta",
                "input_token_cost_per_million": 0.9,
                "output_token_cost_per_million": 0.9,
            },
            "meta-llama/Llama-2-13b-chat-hf": {
                "model": ChatTogether,
                "premium": False,
                "company": "Meta",
                "input_token_cost_per_million": 0.22,
                "output_token_cost_per_million": 0.22,
            },
            "meta-llama/Llama-2-70b-chat-hf": {
                "model": ChatTogether,
                "premium": True,
                "company": "Meta",
                "input_token_cost_per_million": 0.9,
                "output_token_cost_per_million": 0.9,
            },
            "meta-llama/Llama-3-8b-chat-hf": {
                "model": ChatTogether,
                "premium": False,
                "company": "Meta",
                "input_token_cost_per_million": 0.2,
                "output_token_cost_per_million": 0.2,
            },
            "meta-llama/Llama-3-70b-chat-hf": {
                "model": ChatTogether,
                "premium": True,
                "company": "Meta",
                "input_token_cost_per_million": 0.9,
                "output_token_cost_per_million": 0.9,
            },
            "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": {
                "model": ChatTogether,
                "premium": True,
                "company": "Meta",
                "input_token_cost_per_million": 0.7,
                "output_token_cost_per_million": 0.8,
            },
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo": {
                "model": ChatTogether,
                "premium": True,
                "company": "Meta",
                "input_token_cost_per_million": 0.7,
                "output_token_cost_per_million": 0.8,
            },
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": {
                "model": ChatTogether,
                "premium": True,
                "company": "Meta",
                "input_token_cost_per_million": 0.7,
                "output_token_cost_per_million": 0.8,
            },
            "google/gemma-2b-it": {
                "model": ChatTogether,
                "premium": False,
                "company": "Google",
                "input_token_cost_per_million": 0.1,
                "output_token_cost_per_million": 0.1,
            },
            "google/gemma-7b-it": {
                "model": ChatTogether,
                "premium": False,
                "company": "Google",
                "input_token_cost_per_million": 0.2,
                "output_token_cost_per_million": 0.2,
            },
        }

    def get_chat_model(self, model_name: str, temperature: float):
        """
        Get the appropriate chat model based on the model name.

        Args:
            model_name (str): The name of the chat model.
            temperature (float): The temperature setting for the model.

        Returns:
            object: An instance of the chat model.

        Raises:
            ValueError: If an invalid chat model is specified.
        """
        chat_config = self.model_company_mapping.get(model_name)
        if not chat_config:
            raise ValueError(f"Invalid chat model: {model_name}")

        return chat_config["model"](
            model_name=model_name,
            model=model_name,
        )

    def calculate_cost(self, input_string: str, output_string: str, model_name: str):
        """
        Calculate the cost of a chat interaction based on input and output tokens.

        Args:
            input_string (str): The input text.
            output_string (str): The output text.
            model_name (str): The name of the chat model used.

        Returns:
            tuple: A tuple containing (input_token_length, output_token_length, total_cost).
        """
        chat_config = self.model_company_mapping.get(model_name)
        input_token_length = 0
        output_token_length = 0

        if chat_config["company"] == "OpenAI":
            encoding = tiktoken.encoding_for_model(model_name)
            input_token_length = len(encoding.encode(input_string))
            output_token_length = len(encoding.encode(output_string))
        elif chat_config["company"] == "Anthropic":
            anthropic = Anthropic()
            input_token_length = anthropic.count_tokens(input_string)
            output_token_length = anthropic.count_tokens(output_string)
        elif chat_config["company"] in ["Mistral", "Perplexity", "Meta"]:
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            input_token_length = len(encoding.encode(input_string))
            output_token_length = len(encoding.encode(output_string))
        elif chat_config["company"] == "Google":
            tokenizer = tokenization.get_tokenizer_for_model("gemini-1.5-flash-001")
            input_token_length = tokenizer.count_tokens(input_string).total_tokens
            output_token_length = tokenizer.count_tokens(output_string).total_tokens

        input_cost = (
            input_token_length * chat_config["input_token_cost_per_million"] / 1000000
        )
        output_cost = (
            output_token_length * chat_config["output_token_cost_per_million"] / 1000000
        )
        return input_token_length, output_token_length, input_cost + output_cost

    def create_conversation(self, chat, memory, prompt):
        """
        Create a conversation chain using the provided chat model, memory, and prompt.

        Args:
            chat: The chat model instance.
            memory: The conversation memory.
            prompt: The chat prompt template.

        Returns:
            LLMChain: A conversation chain for generating responses.
        """
        return LLMChain(llm=chat, memory=memory, prompt=prompt, verbose=False)
