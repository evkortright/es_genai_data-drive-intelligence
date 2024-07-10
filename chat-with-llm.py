# chat-with-llm.py
from models.models import load_gpt4
llm = load_gpt4()

# ask a question
answer = llm.predict("How is it going?")

print(answer)
