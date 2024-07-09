# models.py
import os
from dotenv import load_dotenv
load_dotenv()

#from langchain.chat_models import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI

def load_gpt3_5():
 os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY_GPT3_5")
 os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_API_BASE_GPT3_5")
 version = os.getenv("AZURE_OPENAI_API_VERSION_GPT3_5")
 deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME_GPT3_5")
 llm = AzureChatOpenAI(openai_api_version=version, azure_deployment=deployment_name)
 return llm

def load_gpt4():
 os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY_GPT4")
 os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_API_BASE_GPT4")
 version = os.getenv("AZURE_OPENAI_API_VERSION_GPT4")
 deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME_GPT4")
 llm = AzureChatOpenAI(openai_api_version=version, azure_deployment=deployment_name)
 return llm
