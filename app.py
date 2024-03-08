from langchain_helper import initialize_components,create_few_shot_selector,get_prompt
from agent import create_agent
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain

def conversational_chat(agent,user_input):   
    result=agent.invoke({"input": user_input},verbose=True)
    # result = chain({"question": query, "chat_history": st.session_state['history']})
    # st.session_state['history'].append((user_input, result))
    return result["output"]

def main():
    st.title("T Shirts Store: Database Chatbot 👕")
    # Initialize components
    llm, embeddings, db = initialize_components()

    # Create vector store for few shots
    example_selector = create_few_shot_selector(embeddings)

    #chain=ConversationChain.from_llm(llm=llm,)
    
    # Create agent
    agent = create_agent(llm, db, get_prompt(example_selector))

    # if 'history' not in st.session_state:
    #     st.session_state['history'] = []

    # if 'generated' not in st.session_state:
    #     st.session_state['generated'] = ["Hello ! Ask me anything in the Database 🤗"]

    # if 'past' not in st.session_state:
    #     st.session_state['past'] = ["Hey ! 👋"]
    
    #container for the chat history
    # response_container = st.container()
    # #container for the user's text input
    # container = st.container()

    # with container:
    #     with st.form(key='my_form', clear_on_submit=True):
            
    user_input = st.text_input("Query:", placeholder="Talk to your data here", key='input')
    submit_button = st.button(label='Submit')
            
    if submit_button and user_input:
        with st.spinner('Processing...'):    
            output =conversational_chat(agent,user_input)
            st.write(output)
            
            # st.session_state['past'].append(user_input)
            # st.session_state['generated'].append(output)
        
    # if st.session_state['generated']:
    #     with response_container:
    #         for i in range(len(st.session_state['generated'])):
    #             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
    #             message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
    



    








    


# st.title("T Shirts Store: Database Chatbot 👕")
# question = st.text_input("Question: ")

# if question:
#     chain = get_few_shot_db_chain()
#     response = chain.run(question)

#     st.header("Answer")
#     st.write(response)

    

if __name__ == "__main__":
    main()
