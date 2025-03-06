import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
#from langchain_community.llms import Ollama #deprecated
from langchain_ollama import OllamaLLM

prompt = ChatPromptTemplate.from_template("Say something about {topic} in just 2 sentences.")
model = OllamaLLM(model="llama3.2:latest")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke({"topic": "New York"})
print(result)


