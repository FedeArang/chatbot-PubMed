def generate_pubmed_query(query, manual_keyword, author, journal, start_date, end_date):
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

    if manual_keyword:
        manual_keywords = manual_keyword.split(", ")
        for keyword in manual_keywords:
            if len(query)>0:
                query += f' AND {keyword}'
            else:
                query += f'{keyword}'
   
    if author:
        authors = author.split(", ")
        for aut in authors:
            if len(query)>0:
                query += f' AND {aut}[Author]'
            else:
                query += f'{aut}[Author]'
    
    if journal:
        if len(query)>0:
            query += f' AND {journal}[Journal]'
        else:
            query += f'{journal}[Journal]'
    
    if (start_date or end_date):
        if not start_date:
            start_date = '1800'
        if not end_date:
            end_date = '3000'
        if len(query)>0:
            query += f' AND {start_date}:{end_date}[dp]'
        else:
            query += f'{start_date}:{end_date}[dp]'
    return query
