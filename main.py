from fastapi import FastAPI, Request
from service.llm_service import LLMService
from fastapi.responses import JSONResponse
from agents.agent_executor import AgentExecutorBuilder

app = FastAPI()
llm_service = LLMService()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    user_type = data.get("user_type")
    query = data.get("query")
    agent = AgentExecutorBuilder(user_type)
    response = agent.run(query)
    return {"user_type": user_type, "query": query, "response": response}
