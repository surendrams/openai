from openai import OpenAI 
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def chat():
    print("■ AI Chatbot (type 'exit' to quit)")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                    ]
        )
        print("AI:", response.choices[0].message.content)
        print("AI:", response.choices[0].message.model_dump())

if __name__ == "__main__":
    chat()
