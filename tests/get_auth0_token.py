import http.client
import json
import os
from dotenv import load_dotenv, find_dotenv

# Get the AUTHO_CLIENT_ID and AUTHO_CLIENT_SECRET credentials.
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTHO_CLIENT_ID = os.environ['AUTHO_CLIENT_ID']
AUTHO_CLIENT_SECRET = os.environ['AUTHO_CLIENT_SECRET']


def get_auth0_access_token():
    conn = http.client.HTTPSConnection("espresso-dev.us.auth0.com")

    request_items = { "client_id": AUTHO_CLIENT_ID, \
                      "client_secret": AUTHO_CLIENT_SECRET, \
                      "audience": "api.espresso.routinew.com", \
                      "grant_type": "client_credentials"
                    }

    payload = json.dumps(request_items)
    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data_json = res.read()
    data_dict = json.loads(data_json)
    access_token = data_dict.get('access_token', None)

    return access_token


if __name__ == '__main__':
    access_token = get_auth0_access_token()
    print(access_token)
