# Check if config.ini exist
import os.path
if not os.path.isfile('./config.ini'):
    import streamlit as st
    openai_api_key = st.secrets['CG_API_KEY']
else:
    import configparser as cp
    # Read config file
    config = cp.ConfigParser()
    config.read('./config.ini')
    openai_api_key = config['OPENAI']['API_KEY']

import os
import openai
# Assign openai_api_key to environment variable
os.environ["OPENAI_API_KEY"]  = openai_api_key
# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")


# Call chatgpt 3.5
def get_chat_response(prompt: str):
    """
    Call chatgpt 3.5
    """
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", temperature = 0,
    messages=[
            {"role": "system", "content": "You are an analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

# if main run this file
if __name__ == "__main__":
    prompt = "I am writing a news release about \"Singapore Armed Forces (SAF) and Republic of Singapore Air Force (RSAF) to conduct Exercise Red Flag 2021\". List the information I need to write the news release."
    print(get_chat_response(prompt))
