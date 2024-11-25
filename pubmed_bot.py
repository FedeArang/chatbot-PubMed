import streamlit as st
import re
from language_to_query import language_to_query
from generate_pubmed_query import generate_pubmed_query
from pymed import PubMed
from summarize_article import summarize_article

def display_message(role, content):
    """
    Display a single message with simple styling using markdown.
    """
    if role == "user":
        st.markdown(f'<div style="text-align: right; margin: 10px; padding: 10px; border-radius: 15px; background-color: #dcf8c6; display: inline-block; float: right; clear: both; max-width: 80%;">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left; margin: 10px; padding: 10px; border-radius: 15px; background-color: #ADD8E6; display: inline-block; float: left; clear: both; max-width: 80%;">{content}</div>', unsafe_allow_html=True)


# Set page config to wide mode
st.set_page_config(layout="wide")

llama_api_key = "" #insert your api key here
model_name = "llama3.1-70b" #name of the model to use for converting the query from natural language and for summarization

# Add custom CSS to reduce padding
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        .element-container {
            margin-bottom: 0.5rem;
        }.scrollable-container {
            height: 70vh;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            padding: 10px;
        }
        
    </style>
""", unsafe_allow_html=True)


# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "pubmed_query" not in st.session_state:
    st.session_state.pubmed_query = None
if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}
if "max_articles" not in st.session_state:
    st.session_state.max_articles = 5
if "refine_query" not in st.session_state:
    st.session_state.refine_query = None
if "clarify_intent" not in st.session_state:
    st.session_state.clarify_intent = None

# Streamlit application
st.title("PubMed Chatbot Interface")

# Create main columns with custom widths
col1, spacer, col2 = st.columns([0.45, 0.05, 0.5])

# Left column: Chat interface
with col1:
    st.subheader("Chat Interface")
    
    # Container for chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message.startswith("User: "):
                display_message("user", message[6:])
            elif message.startswith("AI: "):
                display_message("ai", message[4:])
    
    # Input for chat queries
    if len(st.session_state.chat_history)==0 or st.session_state.refine_query:
        chat_input = st.text_input("", placeholder="Type your query here...", key="chat_input", value="")

        # Send button
        button_col1, button_col2, button_col3 = st.columns([3, 1, 1])
        with button_col3:
            send_pressed = st.button("Send")

        if send_pressed and chat_input.strip():
            st.session_state.chat_history.append(f"User: {chat_input}")
            try:
                st.session_state.parsed_data = language_to_query(chat_input, llama_api_key, model_name)
            except:
                #in case the generation of the query fails, we ask the user to generate a new one
                st.session_state.clarify_intent = True
                st.rerun()
            #if the generated query is empty, ask to produce a new query in natural language
            if not st.session_state.parsed_data:
                st.session_state.clarify_intent = True
                st.rerun()
            st.session_state.chat_history.append("AI: Would you like to provide any additional details (Keywords, Authors, Journal, Date Range)?")
            st.session_state.waiting_for_response = True
            st.session_state.pubmed_query = None
            st.session_state.show_form = False
            st.session_state.refine_query = False
            chat_input = ""  # Clear the chat input after sending
            st.rerun()

    # Handle user input for Yes/No
    if len(st.session_state.chat_history)>0 and st.session_state.chat_history[-1]=="AI: Would you like to provide any additional details (Keywords, Authors, Journal, Date Range)?":
        button_col1, button_col2, button_col3 = st.columns([3, 1, 1])
        with button_col3:
            yes = st.button("Yes")
            no = st.button("No")
            if yes:
                st.session_state.show_form = True
                st.session_state.waiting_for_response = False
                st.session_state.chat_history.append("User: Yes")
                chat_input = ""  # Clear the chat input after receiving response
                st.rerun()
            if no:
                st.session_state.waiting_for_response = False
                st.session_state.chat_history.append("User: No")
                st.session_state.pubmed_query = st.session_state.parsed_data
                chat_input = ""  # Clear the chat input after receiving response
                st.rerun()
                

    # Form for additional details
    if st.session_state.show_form:
        st.write("Please fill out the details below:")
        with st.form("additional_details_form"):
            keywords = st.text_input("Keywords (optional). If multiple, should be separated by commas:", value="")
            authors = st.text_input("Authors (optional). If multiple, should be separated by commas:", value="")
            journal = st.text_input("Journal (optional):", value="")
            start_date = st.text_input("Start Date (YYYY, optional):", value="")
            end_date = st.text_input("End Date (YYYY, optional):", value="")
            st.session_state.max_articles = st.slider("Maximum Number of Articles to Display:", min_value=1, max_value=100, value=5)
            
            if st.form_submit_button("Submit"):
                st.session_state.show_form = False
                st.session_state.chat_history.append("AI: Additional details received. Searching...")
                st.session_state.pubmed_query = generate_pubmed_query(
                    st.session_state.parsed_data, keywords, authors, journal, start_date, end_date
                )
                if not st.session_state.pubmed_query:
                    st.session_state.clarify_intent = True
                st.rerun()

    if len(st.session_state.chat_history)>0 and st.session_state.chat_history[-1]=="AI: Are you satisfied with the results of the query? Do you want to refine the query?":

        button_col1, button_col2= st.columns([1, 2])
        with button_col2:
            next_query = st.button("Yes, I'm satisfied with the current query. Let's go to the next query!")
            modify_query = st.button("I would like to make some modifications to the query")

            #If user is satisfied with the query and wants to go the next query, we initialize everything from scratch
            if next_query:
                st.session_state.chat_history = []
                st.session_state.show_form = False
                st.session_state.pubmed_query = None
                st.session_state.waiting_for_response = False
                st.session_state.parsed_data = {}
                st.session_state.max_articles = 5
                st.session_state.refine_query = None
                st.session_state.clarify_intent = None
                st.rerun()

            if modify_query:
                st.session_state.chat_history.append("User: I would like to make some modifications to the query")
                st.session_state.chat_history.append("AI: Great, let's modify your query! Would you like to add more details to the previous query or you would like to reformulate the query?")
                st.rerun()

    if len(st.session_state.chat_history)>0 and st.session_state.chat_history[-1]=="AI: Great, let's modify your query! Would you like to add more details to the previous query or you would like to reformulate the query?":
        
        button_col1, button_col2= st.columns([1, 2])
        with button_col2:  
            add_details = st.button("I would like to add more details to the previous query")
            modify_query = st.button("I would like to reformulate the query")

            #if the user wants to add more details, we show the form again
            if add_details:

                st.session_state.chat_history.append("User: I would like to add more details to the previous query")
                st.session_state.chat_history.append("AI: Sure! Please add more details in the form below!")
                st.session_state.show_form = True
                st.rerun()

            #Otherwise, we let the user refine the query
            if modify_query:
                st.session_state.chat_history.append("User: I would like to reformulate the query")
                st.session_state.chat_history.append("AI: Sure! Please type your modified query below!")
                st.session_state.pubmed_query = None
                st.session_state.refine_query = True
                st.rerun()

    if st.session_state.clarify_intent:
        st.session_state.chat_history.append("AI: Your query is currently not valid! Please type a new query!")
        st.session_state.pubmed_query = None
        st.session_state.refine_query = True
        st.session_state.clarify_intent = None
        st.rerun()



# Right column: Results
with col2:
    
    

    if st.session_state.pubmed_query:
        st.subheader("Search Results")
        st.write("### Generated PubMed Query:")
        st.code(st.session_state.pubmed_query, language="text")


        # Fetch and display results
        st.write("### Results:")
        pubmed = PubMed(tool="MyTool", email="my@email.address")
        results = list(pubmed.query(st.session_state.pubmed_query, max_results=st.session_state.max_articles))
        if len(results)>0:
            
            for idx, article in enumerate(results):
                with st.expander(f"**{article.title}**"):
                    st.write(f"**Title:** {article.title}")

                    #for some articles the following quantities are not defined, so we need to take care of it via a try/except
                    authors = ''
                    try:
                        for author in article.authors:
                            authors += f' {author["lastname"]} {author["firstname"]},'
                        st.write(f"**Author(s):** {authors[0:-1]}")
                    except:
                        pass
                    
                    try:
                        st.write(f"**Journal:** {article.journal}")
                    except:
                        pass
                    
                    try:
                        st.write(f"**Abstract:** {article.abstract}")
                    except:
                        pass
                    
                    keywords = ''
                    try:
                        for keyword in article.keywords:
                            keywords += f' {keyword},'
                        st.write(f"**Keywords:** {keywords[0:-1]}")
                    except:
                        pass
                    
                    try:
                        st.write(f"'**DOI:** {article.doi}")
                    except:
                        pass
                    
                    
                    if st.button(f"Summarize", key=f"Summarize {idx}"):
                        if article.abstract is None or len(article.abstract)==0:
                            st.write("It is not possible to write a summary since the abstract is not present")
                        else:
                            try:
                                summary = summarize_article(article.abstract, model_name, llama_api_key)
                                st.write(f"**Summary:** {summary}")
                            except:
                                st.write("Sorry, it was not possible to write the summary due to technical issues with the API")

            # Add a message in the chat after displaying results
            if len(st.session_state.chat_history) == 0 or (st.session_state.chat_history[-1] == "User: No" or st.session_state.chat_history[-1]=="AI: Additional details received. Searching..."):
                st.session_state.chat_history.append("AI: Are you satisfied with the results of the query? Do you want to refine the query?")
                st.rerun()
    
            
        else:
            st.write("No results found. Try different query parameters.")
            #if the search did not produce any result, restart the query
            if len(st.session_state.chat_history) == 0 or (st.session_state.chat_history[-1] == "User: No" or st.session_state.chat_history[-1]=="AI: Additional details received. Searching..."):
                st.session_state.chat_history.append("AI: Your query did not produce any result! Please try with a different query!")
                st.session_state.pubmed_query = None
                st.session_state.refine_query = True
                st.rerun()
            
            
    
            
        
            
   


