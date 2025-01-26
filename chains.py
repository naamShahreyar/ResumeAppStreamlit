from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from llm import LLM
from prompts import *


skill_extract_prompt = PromptTemplate(input_variables=["text"], template=extract_skills_prompt_template)
skill_extraction_chain = LLMChain(llm=LLM, prompt=skill_extract_prompt)

parse_resume_prompt = PromptTemplate(input_variables=["text"], template=parse_resume_prompt_template)
parse_resume_chain = LLMChain(llm=LLM, prompt=parse_resume_prompt)