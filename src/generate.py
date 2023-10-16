
def create_prompt_info(seedtitle: str, docs: list):
    """
    Create prompt for OpenAI GPT-3
    """
    similar_docs = ""
    for doc in docs:
        similar_docs += f"""
Title: {doc['title']}
Content: {doc['article']}
        """

    prompt = f'''As a Singaporean analyst, I am currently writing a news release related to the working title: "{seedtitle}". Can you please provide me with a bullet point list of the essential information required for the effective composition of this news release?

Other similar news releases: {similar_docs}

To write a news release about "{seedtitle}", I will need to include the following information:
    '''

    return prompt

def create_prompt_report(seedtitle: str, nr_info: str, docs: list):
    """
    Create prompt for OpenAI GPT-3.5
    """
    similar_docs = ""
    for doc in docs:
        similar_docs += f"""
Title: {doc['title']}
Content: {doc['article']}
        """
    prompt = f'''As a Singaporean analyst, I am currently drafting a news release about "{seedtitle}".

Information I have:
{nr_info}

Writing style to follow:{similar_docs}

As a Singaporean analyst, draft a public news release about the title: "{seedtitle}", using the writing style provided and relying on the information available. I will write:
'''
    
    return prompt