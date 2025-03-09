import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import (
    AgentExecutor,
    create_react_agent
)
from langchain import hub
from tools.tools import get_profile_url_tavily


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    template = """Given the full name of the person {name_of_person} return the twitter profile of the person. 
    Your answer should contain only the twitter username with no formatting"""

    prompt_template = PromptTemplate(
        input_variables=['name_of_person'],
        template=template,
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google for twitter username",
            func=get_profile_url_tavily,
            description="Useful when you want to find the twitter username of a person using google search of their name. You must specify 'Twitter' at the end of the search query",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)})

    return result['output']


if __name__ == '__main__':
    print(lookup('Nabeel Farooqui who works are Folio3 and studied at IBA'))
