from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os

client = OpenAI()
app = FastAPI()

@app.get("/chat")
def chat(message: str):
    def event_stream():
        full_text = ""

        with client.chat.completions.stream(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
        ) as stream:
            for event in stream:
                # Incremental tokens
                if event.type == "content.delta":
                    if event.delta:
                        full_text += event.delta
                        yield event.delta  # plain text chunk

                # Final full message
                elif event.type == "content.done":
                    yield f"\n\n[FINAL]: {event.content}"

    return StreamingResponse(event_stream(), media_type="text/plain")
