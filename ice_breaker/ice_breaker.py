from typing import Tuple

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.linkedind_lookup_agent import lookup as linkedin_lookup_agent
from parsers.output_parser import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template: str = """
            given the LinkedIn information {information} about a person from I want you to create:
            1. a short summary
            2. two interesting facts about them
            
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template,
                                             partial_variables={
                                                 "format_instructions": summary_parser.get_format_instructions()})

    # llm = ChatOllama(model="llama3.2")
    # llm = ChatOllama(model="mistral")

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    result = ice_break_with(name="Nikolas Sturaro, a Software Engineer at Cherry Bank based on Monselice")

    print(result)
