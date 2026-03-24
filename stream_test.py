from openai import OpenAI

client = OpenAI()

def main():
    print("🔄 Streaming from OpenAI...\n")

    full_text = ""

    with client.chat.completions.stream(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain AI in simple words."},
        ],
    ) as stream:
        for event in stream:
            # Handles incremental content
            if event.type == "content.delta":
                if event.delta:
                    print(event.delta, end="", flush=True)
                    full_text += event.delta

            # Handles final full message
            elif event.type == "content.done":
                print("\n\n✅ Final:", event.content)

if __name__ == "__main__":
    main()
