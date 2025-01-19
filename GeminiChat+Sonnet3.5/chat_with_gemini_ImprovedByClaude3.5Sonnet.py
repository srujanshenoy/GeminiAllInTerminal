import os
import sys
import time
from typing import Dict

# Google Generative AI Imports
import google.generativeai as genai
from google.generativeai import types

# Rich Library Imports
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Environment and Configuration Management
from dotenv import load_dotenv

# System Configuration
SYSTEM_INSTRUCTION = """
You are an expert software developer and a helpful coding assistant.
You are able to generate high-quality code in any programming language.
Provide clear, concise, and well-documented responses.
"""

MODELS: Dict[int, str] = {
    1: 'gemini-1.5-pro',
    2: 'gemini-1.5-flash',
    3: 'gemini-pro',
    4: 'gemini-1.0-pro',
}

class GeminiChatAssistant:
    def __init__(self, api_key: str, model_name: str = 'gemini-1.5-pro'):
        """
        Initialize Gemini Chat Assistant
        
        Args:
            api_key (str): Google AI API Key
            model_name (str, optional): Selected Gemini model. Defaults to 'gemini-1.5-pro'.
        """
        genai.configure(api_key=api_key)
        self.console = Console()
        self.model_name = model_name
        self.chat_session = self._create_chat_session()

    def _create_chat_session(self):
        """Create a new chat session with specified configuration"""
        return genai.chat(
            model=self.model_name,
            system_instruction=SYSTEM_INSTRUCTION,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 8192
            }
        )

    def stream_response(self, user_input: str):
        """
        Stream response with markdown rendering
        
        Args:
            user_input (str): User's message to the AI
        """
        try:
            response_chunks = []
            full_response = ""

            # Stream the response
            for chunk in self.chat_session.send_message(user_input, stream=True):
                if chunk.text:
                    response_chunks.append(chunk.text)
                    full_response += chunk.text
                    
                    # Clear console and render markdown
                    self.console.clear()
                    markdown = Markdown(''.join(response_chunks))
                    self.console.print(markdown)
                    time.sleep(0.05)  # Small delay for readability

        except Exception as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")

    def run(self):
        """Main chat interaction loop"""
        self.console.print(Panel.fit(
            f"Gemini Chat Assistant\nModel: {self.model_name}", 
            title="🤖 Welcome", 
            border_style="bold blue"
        ))

        while True:
            try:
                user_input = self.console.input("[bold green]You: [/bold green]")

                if user_input.lower() in ['/exit', '/quit']:
                    break
                elif user_input.lower() == '/clear':
                    self.chat_session = self._create_chat_session()
                    self.console.print("[yellow]Chat session reset.[/yellow]")
                    continue

                self.stream_response(user_input)

            except KeyboardInterrupt:
                self.console.print("\n[bold yellow]Chat terminated.[/bold yellow]")
                break

def select_model() -> str:
    """Model selection interface"""
    print("Available Models:")
    for key, model in MODELS.items():
        print(f"{key}: {model}")
    
    while True:
        try:
            choice = int(input("Select model number: "))
            return MODELS.get(choice, 'gemini-1.5-pro')
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    # Load environment variables
    load_dotenv()

    # Retrieve API Key
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("[ERROR] API Key not found. Please set it up.")
        sys.exit(1)

    # Select and initialize model
    selected_model = select_model()
    chat_assistant = GeminiChatAssistant(api_key, selected_model)
    chat_assistant.run()

if __name__ == "__main__":
    main()