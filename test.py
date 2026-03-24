import asyncio
from agents import Agent, Runner, function_tool

# --- Define tools ---
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."

@function_tool
def calculate(expr: str) -> str:
    try:
        return str(eval(expr))  # ⚠️ unsafe in production; demo only
    except Exception as e:
        return f"Error: {e}"

# --- Define specialist agents ---
english_agent = Agent(
    name="English agent",
    instructions="You are an English-speaking assistant. Answer queries in English."
)

spanish_agent = Agent(
    name="Spanish agent",
    instructions="Eres un asistente que responde solo en español."
)

math_agent = Agent(
    name="Math agent",
    instructions="You are a math expert. Solve math queries directly with the numeric result.",
    tools=[calculate]
)

weather_agent = Agent(
    name="Weather agent",
    instructions="You are a weather assistant. When asked, call the weather tool to get weather for a city.",
    tools=[get_weather]
)

# --- Define the triage agent (router) ---
triage_agent = Agent(
    name="Triage agent",
    instructions="""
    You are a router. Based on the user's input, decide which agent should respond:
    - Spanish agent if the user input is in Spanish
    - Math agent if the user input is math or calculation related
    - Weather agent if it's about weather or asking the city weather
    - Otherwise, English agent
    """,
    handoffs=[english_agent, spanish_agent, math_agent, weather_agent]
)

async def main():
    # Text only
    result1 = await Runner.run(triage_agent, "Hello, how are you?")
    print("Output:", result1.final_output)

    # Spanish
    result2 = await Runner.run(triage_agent, "Hola, ¿cómo estás?")
    print("Output:", result2.final_output)

    # Math
    result3 = await Runner.run(triage_agent, "What is 25 * 4 + 6?")
    print("Output:", result3.final_output)

    # Weather
    result4 = await Runner.run(triage_agent, "What's the weather in Paris?")
    print("Output:", result4.final_output)

if __name__ == "__main__":
    asyncio.run(main())
