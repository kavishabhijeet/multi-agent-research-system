from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrap_url
from dotenv import load_dotenv

load_dotenv()

# model setup
llm = ChatMistralAI(model_name="mistral-small-latest",temperature=0.2)

# 1st Agent
def build_serach_agent():
    return create_agent(
        model = llm,
        tool = [web_search]
    )
# 2nd Agent
def build_reader_agent():
    create_agent(
        model = llm,
        tool = [scrap_url]
    )

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system","You are an expert research writer. Write clear, structured and insightful reports"),
    ("human","""Write a detailed research report on the topic below.
     Topic : {topic}
     Research Gathered : {research}
     Structure thereport as:
     - Introduction
     - Key Findings (minimum 3 well-explained points)
     - Conclusion
     - Sources (List all urls found in the research)

     Be detailed, factual and professional""")
])    
writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system"," You are a sharp and constructive research critic. Be honest and specific."),
    ("human","""Review the research report below and evaluate it strictly.
     Report : {report}
     Respond in this exact formate :
     Score : X/10
     Strengths:
     - ....
     - ....
     Areas to Improve:
     - ...
     - ...
     One Line Verdict:
     ...""")
])
critic_chain = critic_prompt | llm | StrOutputParser()

