from langchain_community.utilities import SQLDatabase
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from few_shots import few_shots

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env 


def initialize_components():
    """Initialize essential components for the agent."""
    llm = ChatOpenAI()
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "store_tshirts"

    db = SQLDatabase.from_uri(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)
    return llm, embeddings, db


def create_few_shot_selector(embeddings):
    example_selector = SemanticSimilarityExampleSelector.from_examples(
                        few_shots,embeddings,Chroma,k=2,input_keys=["input"],)
    return example_selector


def get_prompt(example_selector):
    system_prefix = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
    If the word 'discount' is given in the input query the discounts table also using the t_shirt_id from the t_shirts table and subtract the price.
    In "t_shirts" table "price" column refers to price for a single t shirt and "stock_quantity" refers to number of t-shirts.
    In "discounts" table "pct_discount" refers to the percentage of discount offered.
    If there is no corresponding entry in "discounts" table give the "price" column value in  "t_shirts" table.You can return "There is no discount" as the answer .

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    If the question does not seem related to the database, just return "I don't know" as the answer.

    Here are some examples of user inputs and their corresponding SQL queries:"""

    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix="",
    )

    full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
    )
    return full_prompt