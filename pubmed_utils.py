def extract_pubmed_query(answer, prefix):
    """
    Extracts the PubMed query from the provided answer.

    Parameters:
        answer (str): The response containing the PubMed query in the format 
                      "PubMed Query: <query>".

    Returns:
        str: The extracted query string.
    """

    if prefix in answer:
        return answer.split(prefix, 1)[1].strip()
    
    elif answer == "PubMed Query:":
        return ""
    else:
        raise ValueError(f"Invalid format: {prefix} prefix not found.")
    
