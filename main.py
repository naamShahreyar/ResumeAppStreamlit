import streamlit as st
import pandas as pd
from streamlit_card import card
from Neo4jHandler.initialize_vector_index import vector_index
from Neo4jHandler.initialize_neo4j_handler import neo4j_handler
from chains import skill_extraction_chain
from utils import get_candidate
from params import data_scientist_skills



with st.sidebar:
    required_skillset = st.multiselect(
    "**Filter Based On Skills**",
    data_scientist_skills
    )
    
    results_to_show = st.slider("How Many Results to Show?", 1, 10, 1)
    
    if st.button("**Clear Chat**", type='primary'):
        st.session_state.messages = []


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat messages from history on app rerun

if st.session_state.messages:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                data = pd.DataFrame(message["content"]).head(results_to_show)
                st.dataframe(data)
                
else:
    st.markdown("**Hello! I am your assistant.**")
    st.markdown("**You can search for candidates using the search bar below.**")
    st.markdown("**You can also filter the results based on the skills you are looking for.**")
    
        
        

query = st.chat_input("Search Candidates...")

if query:
    # Display user message in chat message container
    st.chat_message("user").markdown(query)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    with st.container():
        
        # Display assistant response in chat message container
        with st.spinner(text="Searching..."):
            retrieved_results = get_candidate(query,neo4j_handler, vector_index,skill_extraction_chain, skill_list=required_skillset)
            with st.chat_message("assistant"):
                data = pd.DataFrame(retrieved_results).head(results_to_show)
                st.dataframe(data)
            
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": retrieved_results})