from google import genai
from rich import print
from rich.markdown import Markdown
from rich.console import Console

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

def get_history_from_file():
    try:
        from chat_history import chat_session_list_from_file
        return chat_session_list_from_file
    except ImportError:
        return []
    except FileNotFoundError:
        return []

def print_chat_session_rich():
    from chat_history import chat_session_list_from_file

    console = Console()
    
    for message in chat_session_list_from_file:
        markdown = Markdown(f"**{message['author'] + '\\n'}:** {message['content']}")
        console.print(markdown)

def commands():
  print(
      """
      Available Commands:

      > /exit           : End the conversation.
      > /clearcontext   : Clear the chat history and reset context for the model.
      > /print          : Print the chat history.
      > /exitwithprint  : End the conversation and print the chat history.
      > /about          : Print this message.
      > /bye            : End the conversation and export the chat history to a file (chat_session.txt).
      
      To enter a multiline message, start with \"\"\" and end with \"\"\" on a new line.
      """)

def model_select(models_dictionary: dict):
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
        if line.strip() == ('\\' + 'ml'):
            if not lines:
                continue
            else:
                break
        lines.append(line)
    return '\n'.join(lines)

def chat_with_gemini(model_name:str, google_api_key:str, imported:bool, chat_session=None) -> None:
    """Provides a chat interface to interact with Gemini with session memory."""

    model = genai.GenerativeModel(model_name, api_key = google_api_key)
    
    chat_session = [] if chat_session is None else chat_session
    print(f"""
    Starting chat with Gemini. Type 'exit' to end the conversation. INFO:

    model: {model_name}
    chat_session: {chat_session}
    API_KEY: {google_api_key}
    """)

    while True:
        print("You: ", end='')
        first_line = input()
        
        if first_line.startswith('\\ml'):
            user_input = get_multiline_input()
        else:
            user_input = first_line

        match user_input.lower():
            case '/exit':
                break

            case '/clearcontext':
                chat_session = []
                print("Chat history cleared.")
                continue

            case '/print':
                print(chat_session)
                continue

            case '/exitwithprint':
                print(chat_session)
                break

            case '/about':
                commands()
                print(f" model: {model_name} \\n chat_session: {'loaded' if imported else 'not loaded'} \\n API_KEY: (DO NOT SHOW IN PUBLIC) {google_api_key}"
                )
                continue

            case '/bye':
                with open('chat_history.py', 'w') as file:
                    file.write("")
                    file.write("chat_session_list_from_file = " + str(chat_session))
                print("Chat history exported to 'chat_history.py'.")

                break

            case _:
                pass

        chat_session.append({"author": "user", "content": user_input})

        try:
            response = model.generate_content(
                contents='\n'.join([f"{msg['author']}: {msg['content']}" for msg in chat_session])
            )

            # Display the response using rich
            markdown = Markdown(response.text)
            print(markdown)

            chat_session.append({"author": "Gemini", "content": response.text})

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    commands()

    if input("load history from file? anything but no/n for yes, n / no for no.").lower() in ['no', 'n']:
        chat_session = []
        print("Starting a new chat session.")
    else:
        chat_session = get_history_from_file()
        print_chat_session_rich()


    chat_with_gemini(
        model_name=model_select(MODELS),
        chat_session=chat_session,
        imported = True if chat_session else False,
        google_api_key='AIzaSyDVoaZwuxjOnM1RujvsyncUaVS4noskGZs'
    )

# Debug Section
if __name__ != "__main__":
    chat_session = get_history_from_file()
    print_chat_session_rich()