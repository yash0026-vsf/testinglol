from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from config.llm import get_llm
from graph.state import SupportState
from pydantic import BaseModel, Field

class Translation(BaseModel):
    translated_text: str = Field(description="The translated text.")

def receive_query(state: SupportState) -> dict:
    customer_message = state["customer_message"].strip()

    return {
        "processed_message": customer_message,
        "messages": [
            HumanMessage(content=customer_message)
        ],
    }

def finalize_response(state: SupportState) -> dict:
    response = state["response"]
    language = state.get("context", {}).get("language", "English")
    
    if language and language.lower() not in ["english", "unknown", "en"]:
        # Translate the response
        llm = get_llm().with_structured_output(Translation)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Translate the following customer support response into {language}. Return only the translation."),
            ("human", "{response}")
        ])
        chain = prompt | llm
        try:
            res = chain.invoke({"language": language, "response": response})
            response = res.translated_text
        except:
            pass

    return {
        "response": response,
        "messages": [
            AIMessage(content=response)
        ],
    }