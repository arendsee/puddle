import getpass
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

with open("/home/z/.openai_api_key", "r") as fh:
    os.environ["OPENAI_API_KEY"] = fh.read().strip()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the curator of a great museum and answer all questions as gravely as possible"),
    ("user", "{text}")
])

model = ChatOpenAI(model="gpt-4")

parser = StrOutputParser()

chain = prompt | model | parser

def ask(prompt):
    return chain.invoke(prompt)
