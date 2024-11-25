from llamaapi import LlamaAPI
from pubmed_utils import extract_pubmed_query
import json

def language_to_query(question, key, model_name):
    
    llama_api_token = key
    llama = LlamaAPI(llama_api_token)

    prompt = "Your task is to convert the following sentence into a PubMed query. If you think the text cannot produce a meaningful query, your converted query should be the empty string. Your answer should be in the format 'PubMed Query:' followed the converted query. Here is the sentence:"+question
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user","content": prompt}]

    response = llama.run({'model': model_name, 'messages': messages, 'stream': False})
    query = extract_pubmed_query(response.json()['choices'][0]['message']['content'], "PubMed Query: ")

    return query