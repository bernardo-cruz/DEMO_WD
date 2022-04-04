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
