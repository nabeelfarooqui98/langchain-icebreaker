from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
import os
from output_parsers import summary_parser, Summary
from typing import Tuple


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name)
    linkedin_data = scrape_linkedin_profile(linkedin_url, True)

    twitter_username = twitter_lookup_agent(name)

    summary_template = """
        Given the linkedin profile info {information} about a person, create the following
        1. summary
        2. two interesting facts about the person

        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'],
        template=summary_template,
        partial_variables={
            'format_instructions': summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={
        'information': linkedin_data})

    return res, linkedin_data.get('photoUrl')


if __name__ == '__main__':
    print('Ice Breaker Start')
    response = ice_break_with(
        'Nabeel Farooqui who works are Folio3 and studied at IBA')
    print('Done')
