import google.generativeai as genai
import os
import time

# Load API key from .env file
google_api_key = "AIzaSyDVoaZwuxjOnM1RujvsyncUaVS4noskGZs"

# Configure the Generative AI model
genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-2.0-flash-exp')

response = model.generate_content(
    contents='Tell me a story in 300 words.',
    stream=True
)
for chunk in response:
    print(chunk.text, end="")
    time.sleep(0.05)