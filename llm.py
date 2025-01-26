from langchain_google_genai import ChatGoogleGenerativeAI
from secret import Gemini_APi_Key

LLM = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=Gemini_APi_Key
)