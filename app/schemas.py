from pydantic import BaseModel


class Question(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    response: str
