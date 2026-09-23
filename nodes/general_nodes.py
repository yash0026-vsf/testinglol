from graph.state import SupportState
from config.llm import get_llm
from config.knowledge_base import retrieve_knowledge
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class GeneralResponse(BaseModel):
    response: str = Field(description="The response to the customer based on the knowledge base.")

GENERAL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a customer support agent.\nAnswer the user based on this company policy:\n{knowledge}"),
    ("human", "{customer_message}")
])

def handle_pricing_question(state: SupportState) -> dict:
    return _answer_with_kb(state)

def handle_product_question(state: SupportState) -> dict:
    return _answer_with_kb(state)

def handle_other_general(state: SupportState) -> dict:
    return _answer_with_kb(state)

def _answer_with_kb(state: SupportState) -> dict:
    llm = get_llm().with_structured_output(GeneralResponse)
    knowledge = retrieve_knowledge(state["processed_message"])
    chain = GENERAL_PROMPT | llm
    res = chain.invoke({"customer_message": state["processed_message"], "knowledge": knowledge})
    return {"response": res.response}