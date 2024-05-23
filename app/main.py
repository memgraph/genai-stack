from fastapi import FastAPI
from app.database import db
from app import schemas
from app.gpt_handler import gpt_handler
from app.llama_handler import llama_handler
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


# ask Memgraph via GPT
@app.post("/ask/gpt", response_model=schemas.QuestionResponse)
def ask_question(question: schemas.Question):
    response = gpt_handler.get_response(question.question)
    return {"question": question.question, "response": response}


# ask Memgraph via Llama
@app.post("/ask/llama", response_model=schemas.QuestionResponse)
def ask_question(question: schemas.Question):
    response = llama_handler.get_response(question.question)
    return {"question": question.question, "response": response["result"]}
