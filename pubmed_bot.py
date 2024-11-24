import streamlit as st
import re
from language_to_query import language_to_query
from generate_pubmed_query import generate_pubmed_query
from pymed import PubMed

# Streamlit application
st.title("PubMed Chatbot Interface")
st.write("Enter your query in natural language or use the optional fields below for a detailed search.")

#openai key and model to use
openai_key = ''
model = "gpt-4o-mini"


# User inputs
with st.form("query_form"):
    natural_language_query = st.text_area("Natural Language Query:", placeholder="E.g., Find articles about COVID-19 vaccine efficacy by John Doe from 2020 to 2023")
    st.write("Or specify details manually:")
    keyword = st.text_input("Keywords (optional):", value="")
    author = st.text_input("Author (optional):", value="")
    start_date = st.text_input("Start Date (YYYY, optional):", value="")
    end_date = st.text_input("End Date (YYYY, optional):", value="")
    max_articles = st.slider("Maximum Number of Articles to Display:", min_value=1, max_value=20, value=5)
    submitted = st.form_submit_button("Search")

if submitted:
    if natural_language_query.strip():
        # Parse natural language query
        query = language_to_query(natural_language_query, openai_key, model)
    else:
        # Default parsed_data when no natural language query is provided
        query = {"keyword": "", "author": "", "start_date": "", "end_date": ""}

    # Generate PubMed query using both parsed and manual inputs
    pubmed_query = generate_pubmed_query(query, keyword, author, start_date, end_date)
    
    st.write(f"### Generated PubMed Query:")
    st.code(pubmed_query, language="text")

    # Fetch and display results
    st.write("### Results:")
    pubmed = PubMed(tool="MyTool", email="my@email.address")
    results = pubmed.query(pubmed_query, max_results=max_articles)

    if results:
        for article in results:
            st.write(f"**Title:** {article.title}")
            authors=''
            for author in article.authors:
                authors+=f'{author['lastname']} {author['firstname']},'
            st.write(f"**Author(s):** {authors}")
            st.write(f"**Abstract:** {article.abstract[:200]}...")
            st.write("---")
    else:
        st.write("No results found. Try different query parameters.")
