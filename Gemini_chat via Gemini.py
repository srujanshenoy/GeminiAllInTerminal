import os
import json
from google import genai
from google.genai import types
from rich import print
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.text import Text

# Constants
SYSTEM_INSTRUCTION = """
You are an expert software developer and a helpful coding assistant.
You are able to generate high-quality code in any programming language.
"""

MODELS = {
    1: 'gemini-1.5-pro',
    2: 'gemini-1.5-flash',
    3: 'gemini-1.5-flash-8b',
    4: 'gemini-2.0-flash-exp',
    5: 'gemini-exp-1206',
    6: 'gemini-exp-1121',
    7: 'learnlm-1.5-pro-experimental',
    8: 'gemma-2-2b-it',
    9: 'gemma-2-9b-it',
    10: 'gemma-2-27b-it'
}

CHAT_HISTORY_FILE = 'chat_history.json'
COMMANDS = """
    Available Commands:

    > /exit           : End the conversation.
    > /clearcontext   : Clear the chat history and reset context for the model.
    > /print          : Print the chat history.
    > /exitwithprint  : End the conversation and print the chat history.
    > /about          : Print this message.
    > /bye            : End the conversation and export the chat history to a file (chat_history.json).
    > /upload         : Upload a file to the model.
    > /import         : Import chat history from a file.
    > /export         : Export chat history to a file.

    To enter a multiline message, start with \"\"\" and end with \"\"\" on a new line.
    """

def load_chat_history(filename=CHAT_HISTORY_FILE):
     """Loads chat history from a JSON file."""
     try:
         with open(filename, 'r') as f:
             return json.load(f)
     except (FileNotFoundError, json.JSONDecodeError):
         return []

def save_chat_history(chat_history, filename=CHAT_HISTORY_FILE):
     """Saves chat history to a JSON file."""
     with open(filename, 'w') as f:
         json.dump(chat_history, f, indent=4)

def export_chat_history(chat_history, filename):
     """Exports chat history to a specified JSON file."""
     try:
       with open(filename, 'w') as f:
           json.dump(chat_history, f, indent=4)
       print(f"Chat history exported to '{filename}'.")
     except Exception as e:
         print(f"Error exporting chat history: {e}")

def import_chat_history(filename):
     """Imports chat history from a specified JSON file."""
     try:
         with open(filename, 'r') as f:
             chat_history = json.load(f)
         print(f"Chat history imported from '{filename}'.")
         return chat_history
     except (FileNotFoundError, json.JSONDecodeError) as e:
         print(f"Error importing chat history: {e}")
         return []

def print_chat_history(chat_history):
     """Prints the chat history using rich."""
     console = Console()
     for message in chat_history:
         markdown = Markdown(f"**{message['author']}:** {message['content']}")
         console.print(markdown)

def display_commands():
     """Prints available commands."""
     print(COMMANDS)

def select_model(models_dictionary: dict):
     """Model selector to choose Gemini model."""
     print("Select a model:")
     for key, value in models_dictionary.items():
         print(f"{key}: {value}")

     while True:
         try:
             choice = int(input("Enter the number of the model you want to use: "))
             if choice in models_dictionary:
                 return models_dictionary[choice]
             else:
                 print("Invalid model number. Please choose from the available options.")
         except ValueError:
             print("Invalid input. Please enter a number.")

def get_multiline_input():
     """Get multiline input from user."""
     lines = []
     while True:
         line = input()
         if line.strip() == '"""':
             if not lines:
                 continue
             else:
                 break
         lines.append(line)
     return '\n'.join(lines)

def process_user_input(user_input, chat_session, client, model_name, google_api_key):
    """Processes user input and returns a response or None."""
    user_input = user_input.lower()

    match user_input:
        case '/exit':
            return None, True

        case '/clearcontext':
            chat_session = []
            print("Chat history cleared.")
            return chat_session, False

        case '/print':
            print_chat_history(chat_session)
            return chat_session, False

        case '/exitwithprint':
            print_chat_history(chat_session)
            return None, True

        case '/about':
            display_commands()
            print(f" model: {model_name} \n API_KEY: (DO NOT SHOW IN PUBLIC) {google_api_key}")
            return chat_session, False

        case '/bye':
            save_chat_history(chat_session)
            print("Chat history exported to 'chat_history.json'.")
            return None, True

        case '/upload':
            path = input("Path: ")
            try:
                client.files.upload(path=path)
            except Exception as e:
                print(f"An error occurred: {e}")
            return chat_session, False

        case '/import':
            filename = input("Enter the filename to import from: ")
            chat_session = import_chat_history(filename)
            return chat_session, False

        case '/export':
            filename = input("Enter the filename to export to: ")
            export_chat_history(chat_session, filename)
            return chat_session, False

        case _:
            return chat_session, False

def chat_with_gemini(model_name: str, google_api_key: str, system_instruction: str):
        """Provides a chat interface to interact with Gemini with session memory."""

        # client = genai.Client(api_key=google_api_key)
        # streamer_bot = genai.GenerativeModel(model_name)

        client = genai.GenerativeModel(model_name=model_name)
        
        chat_session = client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.5,
            ),
        )
        chat_history = load_chat_history()
        print(f"""
        Starting chat with Gemini. Type '/bye' to end the conversation. INFO:

        model: {model_name}
        chat_session: {chat_session}
        API_KEY: (DO NOT SHOW IN PUBLIC) {google_api_key}
        """)

        while True:
            print("You: ", end='')
            first_line = input()

            if first_line.startswith('"""'):
                user_input = get_multiline_input()
            else:
                user_input = first_line

            updated_chat_session, should_exit = process_user_input(user_input, chat_history, client, model_name, google_api_key)

            if should_exit:
                break

            if updated_chat_session is not None:
                chat_history = updated_chat_session

            if not user_input.startswith('/'):
            #  try:
            #      with Live(console=Console(), screen=True, refresh_per_second=10) as live:
            #          text = Text()
            #          live.update(text)
            #          response = chat_session.send_message(user_input, stream=True)
            #          for chunk in response:
            #              text.append(chunk.text)
            #              live.update(text)

            #      chat_history.append({'author': 'You', 'content': user_input})
            #      chat_history.append({'author': 'Gemini', 'content': text.plain})
            #  except Exception as e:
            #      print(f"An error occurred: {e}")

        #  save_chat_history(chat_history)
                try:
                    console = Console()
                    
                    stream = streamer_bot.generate_content_stream(
                                    model=model_name,
                                    contents=user_input
                                    )

                    for chunk in stream:
                        if chunk.parts:
                            for part in chunk.parts:
                                # Print markdown format for only the new part.
                                console.print(Markdown(part.text), end="", flush=True)
                
                except Exception as e:
                    print(f"An error occurred: {e}")



if __name__ == "__main__":
    display_commands()
    api_key = 'AIzaSyDVoaZwuxjOnM1RujvsyncUaVS4noskGZs'
    if not api_key:
        print("Please set the GOOGLE_API_KEY environment variable.")
        exit()

    chat_with_gemini(
        model_name=select_model(MODELS),
        google_api_key=api_key,
        system_instruction=SYSTEM_INSTRUCTION
    )
