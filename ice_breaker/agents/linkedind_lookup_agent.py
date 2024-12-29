import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page. 
                  Your answer should contain only a URL"""
    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)
    tools_for_agent = [
        Tool(name="Crawl Google 4 linkedin profile page",
             func=get_profile_url_tavily,
             description="useful for when you need get the Linkedin Page URL")
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    linked_profile_url = result["output"]

    return linked_profile_url


if __name__ == "__main__":
    linkedin_url = lookup("Nikolas Sturaro, a Software Engineer at Cherry Bank based on Monselice")
    print(linkedin_url)
