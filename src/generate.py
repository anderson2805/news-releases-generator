
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

    prompt = f'''As a Singaporean analyst, I am currently writing a news release regarding the "{seedtitle}". Can you please provide me with a list of the necessary information that I will need in order to compose this news release effectively?

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

As a Singaporean analyst, draft a public news release about "{seedtitle}", using the writing style provided and relying on the information available. I will write:
'''
    
    return prompt