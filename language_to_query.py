import openai
from pubmed_utils import extract_pubmed_query

def language_to_query(question, openai_key, model):
    
    #openai.api_key = openai_key
    seed = 42

    prompt = "Your task is to convert the following sentence into a PubMed query. Your answer should be in the format 'PubMed Query:' followed the converted query. Here is the sentence:"+question
    messages = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user","content": prompt}]

    completion = openai.ChatCompletion.create(model=model, messages=messages, seed = seed)
    query = extract_pubmed_query((completion.choices[0].message)['content'])
    messages.append(completion['choices'][0]['message'])

    return query