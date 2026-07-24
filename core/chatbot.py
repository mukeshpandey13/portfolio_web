import os
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.load import load
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template.json")

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    prompt_data = json.load(f)

template = load(prompt_data)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

chain = template | model


def get_bot_response(question: str, chat_history_raw: list) -> str:
    """
    chat_history_raw: list of dicts like [{"role": "human", "content": "..."}, {"role": "ai", "content": "..."}]
    Returns the bot's reply as a string.
    """
    chat_history = []
    for msg in chat_history_raw:
        if msg["role"] == "human":
            chat_history.append(HumanMessage(content=msg["content"]))
        else:
            chat_history.append(AIMessage(content=msg["content"]))

    response = chain.invoke({
        "chat_history": chat_history,
        "question": question
    })
    return response.content