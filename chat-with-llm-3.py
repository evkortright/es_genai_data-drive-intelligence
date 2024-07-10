# chat-with-llm.py
from models.models import load_gpt4
from langchain.prompts import ChatPromptTemplate
import langchain

langchain.debug = True

llm = load_gpt4()

# create a prompt from a template
prompt = ChatPromptTemplate.from_template(
 "list three benefits of {topic}"
)
# create the chain
chain = prompt | llm

# ask a question
answer = chain.invoke({"topic": "Artificial Intelligence"})
print(answer.content)
