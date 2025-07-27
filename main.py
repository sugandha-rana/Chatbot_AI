from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.agent_executor import AgentExecutorBuilder
from utils.logger import setup_logger

app = FastAPI()

logger = setup_logger("crowdguard", "logs/crowdguard.log")

@app.post("/generate")
async def generate_content(request: Request):
    try:
        data = await request.json()
        user_type = data.get("user_type")
        query = data.get("query")

        logger.info(f"Received request with user_type: {user_type}, query: {query}")

        if not user_type:
            return JSONResponse(status_code=400, content={"error": "Missing user_type"})
        if not query:
            return JSONResponse(status_code=400, content={"error": "Missing query"})

        agent = AgentExecutorBuilder(user_type).create()
        logger.info("AgentExecutor created, running query...")
        response = agent.run(query)
        logger.info(f"Agent response: {response}")

        return response

    except Exception as e:
        logger.error(f"Exception in /generate endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )
