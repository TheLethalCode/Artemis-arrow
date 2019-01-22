import json, os
import requests as rq

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CALL_BACK = 'https://localhost/oauth2callback'

def ret_auth_url():

    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    SCOPES = 'https://www.googleapis.com/auth/youtube'

    params = {
        "scope" : SCOPES,
        "access_type" : "offline",
        "include_granted scopes" : "true",
        "redirect_uri" : CALL_BACK,
        "response_type" : "code",
        "client_id" : CLIENT_ID
    }

    return AUTH_URL, params
    

def ret_token(code,refresh=False):

    POST_URL = "https://www.googleapis.com/oauth2/v4/token"    
    payload = {
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET,
        "code" : code
    }

    if not refresh:
        payload["redirect_uri"] = CALL_BACK
        payload["grant_type"] = "authorization_code"
    
    else:
        payload["grant_type"] = "refresh_token"

    resp = rq.post(POST_URL,payload)
    
    if resp.status_code != 200:
        return -1
    
    return resp.json()


if __name__ == '__main__':
    print(ret_auth_url())
