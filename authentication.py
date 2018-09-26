import os
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build

def get_authenticated_service():

    """ 
    Gets the required credentials using the client id of the app
    """

    CLIENT_SECRETS_FILE = "client_secret.json"
    CREDENTIALS_FILE = "credentials.json"
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    store = file.Storage(CREDENTIALS_FILE)
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        creds = tools.run_flow(flow, store)

    service = build(API_SERVICE_NAME, API_VERSION, http=creds.authorize(Http()))
    return service
