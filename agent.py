from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit


def create_agent(llm, db, full_prompt):
    return create_sql_agent(
        llm=llm,
        toolkit = SQLDatabaseToolkit(llm=llm,db=db),
        prompt=full_prompt,
        verbose=True,
        agent_type='openai-tools',
    )
