from langfuse import get_client
import asyncio
from agents import Agent, Runner
import os
from dotenv import load_dotenv
import logfire
import nest_asyncio
nest_asyncio.apply()
load_dotenv()
 
# Get keys for your project from the project settings page: https://cloud.langfuse.com
os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")    
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY") 
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST")

 
# Your openai key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

 
# Configure logfire instrumentation.
logfire.configure(
    service_name='my_agent_service',
    send_to_logfire=False,
)
# This method automatically patches the OpenAI Agents SDK to send logs via OTLP to Langfuse.
logfire.instrument_openai_agents()
 
langfuse = get_client()
 
# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")
    
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model="gpt-4o-mini"
    )
 
    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)

result =  asyncio.run(main())

