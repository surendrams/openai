from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import asyncio

client = OpenAI()
app = FastAPI()

@app.get("/chat")
async def chat(message: str):
    async def event_stream():
        full_text = ""

        def blocking_stream():
            with client.chat.completions.stream(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message},
                ],
            ) as stream:
                for event in stream:
                    yield event

        # Run blocking OpenAI stream in a thread
        iterator = blocking_stream()
        while True:
            event = await asyncio.to_thread(next, iterator, None)
            if event is None:
                break

            if event.type == "content.delta":
                if event.delta:
                    full_text += event.delta
                    yield event.delta

            elif event.type == "content.done":
                yield f"\n\n[FINAL]: {event.content}"

    return StreamingResponse(event_stream(), media_type="text/plain")
    
    # Make this change below to make it SSE
    # SSE requires `text/event-stream`
    # return StreamingResponse(event_stream(), media_type="text/event-stream")