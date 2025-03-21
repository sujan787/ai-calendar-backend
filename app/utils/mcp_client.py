# Create server parameters for stdio connection
import sys
import os
import asyncio
import traceback
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

load_dotenv()

api_key = os.getenv("CLAUDE_API_KEY")

if not api_key:
    raise ValueError("CLAUDE_API_KEY is missing. Set it in the .env file.")

model = ChatAnthropic(
    model="claude-3-opus-20240229",
    temperature=0.7,
    anthropic_api_key=api_key
)

server_params = StdioServerParameters(
    command=sys.executable,  
    args=["app/mcp/server.py"],
    debug=True 
)

async def run_agent(query:str):
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # await asyncio.sleep(2)
                tools = await load_mcp_tools(session)
                agent = create_react_agent(model, tools)
                agent_response = await agent.ainvoke({"messages": query})
                return agent_response
            
    except Exception as e:
        print("❌ Error occurred:")
        print( str(e))
        traceback.print_exc()

def agent_invoke(query: str) -> str:
    print("Starting AI Agent...")
    result = asyncio.run(run_agent(query))
    result = result['messages'][-1].content if result['messages'][-1].content else ""
    print(result)
    return result;

    
        

