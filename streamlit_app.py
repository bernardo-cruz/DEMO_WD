import streamlit as st
import pandas as pd
import numpy as np

# Import Watson modules
from ibm_watson import AssistantV1, AssistantV2, DiscoveryV1, DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

st.set_page_config(
    page_title = 'Crealogix Discovery',
    layout="wide",
    )
# 
credentials = {
    "own_watson" : {
        "ASSISTANT": {
            "API_KEY": "hD3rHMnUprgYgbU9ltg1hzZ4uAoCRrQ6LZEBh-Eep41u",
            "URL": "https://api.eu-de.assistant.watson.cloud.ibm.com/instances/2518e862-7a58-438b-ab89-76fe5e566e5f",
            "VERSION": "2021-06-14",
        },
        "DISCOVERY":{
            "API_KEY": "yYJXPctXaXV0_f4V8TEvtGp2Ra5tFv3b3wJFowgofKfy",
            "URL": "https://api.eu-gb.discovery.watson.cloud.ibm.com/instances/10319f3c-bf82-4e41-a8c5-350094035fec",
            "VERSION": "2019-04-30",
        },
    },
}

# Connect to Assistant
authenticator = IAMAuthenticator(credentials['own_watson']['ASSISTANT']['API_KEY'])
assistant = AssistantV1(
    version = credentials['own_watson']['ASSISTANT']['VERSION'],
    authenticator = authenticator,
)
assistant.set_service_url(credentials['own_watson']['ASSISTANT']['URL'])

# Connect to DiscoveryV1
authenticator = IAMAuthenticator(credentials['own_watson']['DISCOVERY']['API_KEY'])
discovery = DiscoveryV1(
    version = credentials['own_watson']['DISCOVERY']['VERSION'],
    authenticator = authenticator,
)
discovery.set_service_url(credentials['own_watson']['DISCOVERY']['URL'])

# get environment details
environments = discovery.list_environments().get_result()['environments']
environments = [(item['environment_id'],item['name']) for item in environments if item['name'] == 'CLX_Butler_Environment']
environment_id = environments[0][0]
environment_name = environments[0][1]

# get collection details
collections = discovery.list_collections(environment_id).get_result()
collections = [(item['collection_id'],item['name']) for item in collections['collections'] if item['name'] == 'DEV2_NottingHamBuildingSociety']
collection_id = collections[0][0]
collection_name = collections[0][1]

# Page details
st.image("./images/crealogix_logo.png", width=200)
st.title("Welcome to the Crealogix Discovery Assistant")
#opt = ['Write your own query','Use default query']

# #st.subheader("Would you like to write your own query or use the default query?")
# genre = st.radio(
#      ""
#      (opt[0],opt[1]))

# if genre == opt[0]:
#     st.write(f'Your selection: {opt[0]}')
#     user_input = st.text_input("Enter your query", value = "")

# elif genre == opt[1]: 
#     st.write(f'Your selection: {opt[1]}')
#     QA = [
#         "What is remortgaging?",
#         "Why would you need to remortgage?",
#         "Can I remortgage?",
#         "When can you remortgage?",
#         "Is remortgaging always possible?",
#         "The remortgaging process",
#         "How long does remortgaging take?",
#         "Do I have to have my house valued for a remortgage?",
#         "How do I get my house valued for a remortgage?",
#         "Can I remortgage with the same lender?",
#         "How often can I remortgage?",
#         "Do I need to remortgage if I want to build an extension?",
#         "What are remortgage legal fees?",
#         "Do I need a solicitor for a remortgage?",
#         "What are the costs of remortgaging?",
#         "What's an early repayment charge?",
#         "Can I remortgage to release equity?",
#         "Can I remortgage with a bad credit rating?",
#         "Should I remortgage to consolidate debt?",
#         "Should I remortgage to get a better interest rate?",
#     ]

#     user_input = st.radio(
#         "Select a question", 
#         (item for item in QA))


user_input = st.text_input("Search for:", value = "")

if user_input:
    # get all documents
    documents = discovery.query(
        environment_id = environment_id, 
        collection_id = collection_id,
        filter = '',
        natural_language_query = f'{user_input}',
        passages = False,
        count = 100,
    ).get_result()

    st.text("Your answer:")
    # documents
    {k:v for k,v in documents.items() if k in ['matching_results','results']}
    #st.write([doc['answer'],doc[] for doc in documents['results']])
