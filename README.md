The following ChatBot, whose goal is to retrieve articles from PubMed in an interactive way, is based on the pymed repository (https://github.com/gijswobben/pymed), from which we started. This repository allows users to make queries in the PubMed language and retrieve results in an easy and clean way, without having to deal with the more complex PubMed API. This allows us to easily integrate the code from the repo into our chatbot. In particular, the chatbot converts queries in natural language into queries in the PubMed language, which can then be used to retrieve the articles with features such as authors, journal, abstract and more. To convert queries in natural language into queries in the PubMed language we use the LlamaAPI (https://www.llama-api.com/) with the "llama3.1-70b" model. This allows us to convert complex natural language queries into queries in natural language very easily. Users should get a private token or key to make use of the API and the ChatBot. We note that users can also select different models from the API by changing "model_name" in "pubmed_bot.py".

## Structure and Layout

The ChatBot layout consists of two columns. In the left column, the interactive chat is displayed, where users type queries and a conversational agent replies in an interactive manner. In the right column, the results of the queries are displayed. In particular, we display the resulting query in the PubMed language (we thought this is a nice extra feature to have) and the titles of the papers corresponding to the outcome of the queries. Users can then fetch additional information about the papers (e.g. authors, journal, abstract, keywords and DOI when available (since in some cases some of these features are not given)) by clicking on the title. Furthermore, in addition to the details of the papers, we added an additional button "Summarize" which prompts Llama3.1-70b to summarize the abstract of the paper (when this is available) and displays the summary.

The logic of the chat/conversational AI agent is the following: at first, the user is asked to enter a query in natural language. After this, the query is passed to Llama3.1-70b which transforms this in a query which can be used to retrieve PubMed articles. Note that if the query in natural language produces an empty query (this is the case if the query in natural language does not specify any topic/features of papers, e.g. if the query is "Hi! How are you?"), then the Agent will say that the natural language query produced an empty query and the user is asked to enter a new natural language query. If the query is not empty, the user will be asked if he wants to add additional details to the query. Two buttons with "Yes" or "No" will be displayed in the chat. If the users answers "No", then the ChatBot will use the query to retrieve the articles. If the user answers "Yes", a form is displayed in the chat with features such as "keywords", "authors", "Journal", "Start/End Date" and "Max Numbers of displayed articles" the user can choose. The user can enter multiple keywords and multiple authors but only a single journal. Furthermore, the user can select either only the Start Date or the End Date or both. Note that all these features are optional and the user can choose which ones to insert. "Max Numbers of displayed articles" is a slidebar from which the user can select what is the maximum numbers of articles he wants to be displayed in the right column. The slidebar goes from 1 to 100 and the default value is 5. All these numbers can be easily changed in "pubmed_bot.py". After this, the augmented query will be used to retrieve the articles which will be displayed on the right column. If the search results in no articles, the user is told that his query did not produce any result and is asked to enter a new query. Otherwise, the list of the titles (which, as we mentioned, can be fetched by the user to get additional details) is displayed. After the list of the articles is displayed, the user is asked if he is satisfied with the results of the query or if he wants to refine the query. Two buttons will appear in the chat, i.e. "Yes, I'm satisfied with the current query. Let's go to the next query!" and "I would like to make some modifications to the query". If the user presses the first, the chat and the results will be deleted and a new query will begin. In the user presses the second, he will be asked if he/she would like to add details to the query or if he would like to reformulate the query. Again, two buttons will be displayed in the chat, namely "I would like to add more details to the previous query" and "I would like to reformulate the query". If the user presses the first, the form similar to the above with features such as "keywords", "authors", "Journal" and "Start/End Date" will be displayed. The features the user will insert will be added to the query and the updated results will be displayed on the right column. If the user presses the second, he will have the chance to type a new query from the beginning. This has the same effect as starting from scratch, except from the fact that the previous chat will not be deleted in this case.

## Run the Code

To run the code, users need to first insert their LlamaAPI key in "pubmed_bot.py".\
After that, they need to run:

```python
python pubmed_bot.py
```


## Example Queries
In the following, we will make a couple of example queries and interactions. Note that due to the fact that we use LLMs to produce queries, the final results might vary.

# Example 1

Example Chat
- Natural Language Query:


# Example 2

Example Chat
- User: I would like you to find the papers regarding Active Inference from Karl Friston
- AI: Would you like to provide any additional details (Keywords, Authors, Journal, Date Range)?
- User: No
[Displayed papers: Supervised structure learning, Associative Learning and Active Inference., Homo erectus' slowly broadening Zone of Bounded Surprisals opened the way to technological culture: Reply to comments on "'Snakes and ladders' in palaeoanthropology: From cognitive surprise to skilfulness a million years ago," by., Narrative as active inference: an integrative account of cognitive and social functions in adaptation., Forgetting ourselves in flow: an active inference account of flow states and how we experience ourselves within them.]
- AI: Are 

## Notes on the API
The original documentation of the PubMed API can be found here: [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/tools/developers/). PubMed Central kindly requests you to:

> - Do not make concurrent requests, even at off-peak times; and
> - Include two parameters that help to identify your service or application to our servers
>   * _tool_ should be the name of the application, as a string value with no internal spaces, and
>   * _email_ should be the e-mail address of the maintainer of the tool, and should be a valid e-mail address.

## Notice of Non-Affiliation and Disclaimer 
The author of this library is not affiliated, associated, authorized, endorsed by, or in any way officially connected with PubMed, or any of its subsidiaries or its affiliates. The official PubMed website can be found at https://www.ncbi.nlm.nih.gov/pubmed/.
