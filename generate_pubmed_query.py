def generate_pubmed_query(query, manual_keyword, author, start_date, end_date):
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
        if len(query)>0:
            query += f' AND {manual_keyword}'
        else:
            query += f'{manual_keyword}'
   
    if author:
        if len(query)>0:
            query += f' AND {author}[Author]'
        else:
            query += f'{author}[Author]'
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
