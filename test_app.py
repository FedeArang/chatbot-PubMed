import streamlit as st
import re

def parse_query(user_input):
    """
    Parses a natural language query into structured components for PubMed search.

    Parameters:
        user_input (str): The user's natural language query.

    Returns:
        dict: Parsed query components (keywords, author, date range).
    """
    keyword_match = re.search(r"about (.+?)(?: by| from|$)", user_input)
    author_match = re.search(r"by ([\w\s]+)", user_input)
    date_range_match = re.search(r"from (\d{4}) to (\d{4})", user_input)
    
    return {
        "keyword": keyword_match.group(1).strip() if keyword_match else "",
        "author": author_match.group(1).strip() if author_match else "",
        "start_date": date_range_match.group(1) if date_range_match else "",
        "end_date": date_range_match.group(2) if date_range_match else ""
    }

def generate_pubmed_query(parsed_data, manual_keyword, author, start_date, end_date):
    """
    Converts user inputs and parsed data into a PubMed search query string.

    Parameters:
        parsed_data (dict): Parsed query data (from natural language).
        manual_keyword (str): Manually entered keyword.
        author (str): Author name.
        start_date (str): Start date for the query.
        end_date (str): End date for the query.

    Returns:
        str: PubMed query string.
    """
    # Use parsed data from natural language query if present, otherwise fall back to manual inputs
    query = parsed_data.get("keyword", manual_keyword) or manual_keyword
    if author or parsed_data.get("author"):
        query += f' AND {author or parsed_data["author"]}[Author]'
    if (start_date and end_date) or (parsed_data.get("start_date") and parsed_data.get("end_date")):
        query += f' AND {start_date or parsed_data["start_date"]}:{end_date or parsed_data["end_date"]}[dp]'
    return query

def fetch_dummy_results(max_articles):
    """
    Simulates fetching results from PubMed.

    Parameters:
        max_articles (int): The maximum number of articles to display.

    Returns:
        list: List of dictionaries with dummy article data.
    """
    all_results = [
        {"author": "John Doe", "title": "COVID-19 Vaccine Efficacy in 2021", "abstract": "This study explores the efficacy of COVID-19 vaccines..."},
        {"author": "Jane Smith", "title": "Advances in Diabetes Research", "abstract": "A comprehensive review of recent diabetes treatments..."},
        {"author": "Alice Brown", "title": "Impact of Diet on Diabetes", "abstract": "This paper examines how diet affects diabetes outcomes..."},
        {"author": "Bob Johnson", "title": "New Insights in Vaccinology", "abstract": "A study focusing on novel vaccine development techniques..."},
    ]
    # Limit results to the specified maximum number
    return all_results[:max_articles]

# Streamlit application
st.title("PubMed Chatbot Interface")
st.write("Enter your query in natural language or use the optional fields below for a detailed search.")

# User inputs
with st.form("query_form"):
    natural_language_query = st.text_area("Natural Language Query (optional):", placeholder="E.g., Find articles about COVID-19 vaccine efficacy by John Doe from 2020 to 2023")
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
        parsed_data = parse_query(natural_language_query)
    else:
        # Default parsed_data when no natural language query is provided
        parsed_data = {"keyword": "", "author": "", "start_date": "", "end_date": ""}

    # Generate PubMed query using both parsed and manual inputs
    pubmed_query = generate_pubmed_query(parsed_data, keyword, author, start_date, end_date)
    
    st.write(f"### Generated PubMed Query:")
    st.code(pubmed_query, language="text")

    # Fetch and display results
    st.write("### Results:")
    results = fetch_dummy_results(max_articles)
    if results:
        for article in results:
            st.write(f"**Title:** {article['title']}")
            st.write(f"**Author(s):** {article['author']}")
            st.write(f"**Abstract:** {article['abstract'][:200]}...")
            st.write("---")
    else:
        st.write("No results found. Try different query parameters.")
