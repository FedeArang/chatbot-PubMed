from llamaapi import LlamaAPI
import json
from pubmed_utils import extract_pubmed_query

def summarize_article(article, model_name, key):

    llama_api_token = key
    llama = LlamaAPI(llama_api_token)

    prompt = "Your task is to summarize the following abstract of a scientific article. Your output should be in the format 'Summary:' followed by your summary. Here is the abstract:"+article
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user","content": prompt}]

    response = llama.run({'model': model_name, 'messages': messages, 'stream': False})
    print(prompt)
    print(response.json()['choices'][0]['message']['content'])
    summary = extract_pubmed_query(response.json()['choices'][0]['message']['content'], "Summary: ")
    

    return summary