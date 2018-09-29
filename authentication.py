import os
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.discovery import build

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():

    """ 
    Gets the required credentials using the client id of the app that gives full access to the user's data
    """

    CLIENT_SECRETS_FILE = "client_secret.json"
    CREDENTIALS_FILE = "credentials.json"
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    
    store = file.Storage(CREDENTIALS_FILE)
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        creds = tools.run_flow(flow, store)

    service = build(API_SERVICE_NAME, API_VERSION, http=creds.authorize(Http()))
    return service

def get_normal_service():
    """
    Gets the normal service that doesn't require access to user's data
    """

    DEVELOPER_KEY = "AIzaSyDRMJBqNuieYDhHiw4rHWT0fBUWe_EzcJk"
    service = build(API_SERVICE_NAME,API_VERSION,developerKey=DEVELOPER_KEY)
    return service

if __name__ == '__main__':
    service = get_normal_service()
    resp = service.search().list(q='hi',part='snippet').execute()
    print(resp)