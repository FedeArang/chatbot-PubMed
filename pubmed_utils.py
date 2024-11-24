def extract_pubmed_query(answer):
    """
    Extracts the PubMed query from the provided answer.

    Parameters:
        answer (str): The response containing the PubMed query in the format 
                      "PubMed Query: <query>".

    Returns:
        str: The extracted query string.
    """
    prefix = "PubMed Query: "
    if prefix in answer:
        return answer.split(prefix, 1)[1].strip()
    else:
        raise ValueError("Invalid format: 'PubMed Query:' prefix not found.")
