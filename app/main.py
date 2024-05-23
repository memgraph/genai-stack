from fastapi import FastAPI
from app.database import db
from app import schemas
from app.langchain_handler import langchain_handler
from app.ollama_handler import ollama_handler
import logging


app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up and checking database connection...")
    try:
        # Test database connection
        with db.get_session() as session:
            session.run("RETURN 1")
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Failed to establish database connection: {e}")
        raise e


# ask Memgraph via OpenAI
@app.post("/ask/openai", response_model=schemas.QuestionResponse)
def ask_question(question: schemas.Question):
    response = langchain_handler.get_response(question.question)
    return {"question": question.question, "response": response}


# ask Memgraph via Ollama
@app.post("/ask/ollama", response_model=schemas.QuestionResponse)
def ask_question(question: schemas.Question):
    response = ollama_handler.get_response(question.question)
    return {"question": question.question, "response": response["result"]}
