# Chat with MySql DB using Open AI with Lang Chain SQL Agents
The goal of the project is to create a QA engine which can take user questions about database,convert to SQL query using the SQL Agent and
return the corresponding query response in a user readable answer format. Few shot examples are also provided to give sample complex queries.
Screenshot of the application is as below:

![Screenshot_SQL_QA](https://github.com/sunithalv/chat_db_sql/assets/28974154/4ca1a375-4fff-4dc9-a37f-a0ab63de61ba)


## Tech Used
1. ChatOpenAI
2. LangChain
3. ChromaDB
4. Streamlit
5. MYSQL


## Run the Application

### Step 1-: Clone the Repository
```
git clone https://github.com/sunithalv/chat_db_sql.git
```

### Step 2-: Create conda environment
```
conda create -n myenv python==3.10 -y
```

### Step 3-: Activate Conda environment
```
conda activate myenv
```

### Step 4-: Install requirements
```
pip install -r requirements.txt
```

### Step 5-: .env file
```
OPENAI_API_KEY= 

```

### Step 6-: Run the application 
```
streamlit run app.py
```
