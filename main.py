from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agents.agent_executor import AgentExecutorBuilder
from utils.logger import setup_logger
from session_manager import session_manager

app = FastAPI(title="CrowdGuard AI", description="AI-powered crowd management system")

logger = setup_logger("crowdguard", "logs/crowdguard.log")

@app.get("/")
async def root():
    """Root endpoint to check if server is running"""
    return {"message": "CrowdGuard AI Server is running!", "endpoints": ["/generate"]}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T12:00:00Z"}

@app.post("/generate")
async def generate_content(request: Request):
    try:
        logger.info("Received request to /generate endpoint")
        data = await request.json()
        user_type = data.get("user_type")
        query = data.get("query")
        session_id = data.get("session_id")  # Optional session ID

        logger.info(f"Received request with user_type: {user_type}, query: {query}, session_id: {session_id}")

        if not user_type:
            return JSONResponse(status_code=400, content={"error": "Missing user_type"})
        if not query:
            return JSONResponse(status_code=400, content={"error": "Missing query"})

        # Handle session management
        if session_id:
            # Use existing session
            session = session_manager.get_session(session_id)
            if not session:
                return JSONResponse(status_code=400, content={"error": "Session expired or invalid"})
            chat_history = session_manager.get_chat_history(session_id)
        else:
            # Create new session
            session_id = session_manager.create_session(user_type)
            chat_history = []

        agent = AgentExecutorBuilder(user_type).create()
        logger.info("AgentExecutor created, running query...")
        
        response = agent.run({"input": query, "chat_history": chat_history})
        logger.info(f"Agent response: {response}")

        # Add to session history
        response_text = response.get("output", str(response)) if isinstance(response, dict) else str(response)
        session_manager.add_to_history(session_id, query, response_text)

        return {
            "response": response,
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"Exception in /generate endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )
