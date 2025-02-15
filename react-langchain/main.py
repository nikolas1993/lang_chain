from typing import Union

from dotenv import load_dotenv
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """"Return the length of the text"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip('"')  # stripping away non alphabetic characters just in case
    return len(text)


if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    tools = [get_text_length]
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    
    Begin!
    
    Question: {input}
    Thought:
    """


## Thought: I now know the final answer
## Final Answer: the final answer to the original input question
    prompt = PromptTemplate.from_template(template=template).partial(tools=render_text_description(tools),
                                                                     tool_names=", ".join(t.name for t in tools))

    llm = ChatOpenAI(temperature=0, stop=["\nObservation"])

    agent = {"input": lambda x: x["input"]} | prompt | llm | ReActSingleInputOutputParser()

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({"input": "What is the length of 'DOG' in characters?"})

    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        ##tool_to_use = find_tool_by_name(tools, tools)