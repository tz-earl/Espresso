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

AUTH0_BARISTA_TEST_USER_NAME = os.environ['AUTH0_BARISTA_TEST_USER_NAME']
AUTH0_BARISTA_TEST_USER_PASSWORD = os.environ['AUTH0_BARISTA_TEST_USER_PASSWORD']

AUTH0_PASSWORD_GRANT = 'password'
AUTH0_CLIENT_CRED_GRANT = 'client_credentials'
AUTH0_CRU_RESTAURANTS_SCOPE = "read:restaurants create:restaurants update:restaurants"


def get_auth0_access_token(grant_type, scope=None):
    """Retrieves an access token using the Auth0 Client Credentials Flow
    which is documented at https://auth0.com/docs/flows/client-credentials-flow
    and at https://auth0.com/docs/api/authentication#client-credentials-flow
    """
    conn = http.client.HTTPSConnection("espresso-dev.us.auth0.com")

    request_items = { "client_id": AUTHO_CLIENT_ID, \
                      "client_secret": AUTHO_CLIENT_SECRET, \
                      "audience": "api.espresso.routinew.com", \
                      "grant_type": grant_type
                     }
    if grant_type == AUTH0_PASSWORD_GRANT:
        request_items.update({ "username": AUTH0_BARISTA_TEST_USER_NAME, \
                               "password": AUTH0_BARISTA_TEST_USER_PASSWORD, \
                               "scope": scope
                             })
    elif grant_type == AUTH0_CLIENT_CRED_GRANT:
        pass  # Nothing else to add to the request
    else:
        assert(False, "Invalid grant type passed as parameter")

    payload = json.dumps(request_items)
    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data_json = res.read()
    data_dict = json.loads(data_json)
    access_token = data_dict.get('access_token', None)

    return access_token


# Get the Auth0 access token just once to avoid repeated hits to the Auth0 API
# "cru" means permissions to create-read-update
access_token_cru_restaurants = get_auth0_access_token(AUTH0_PASSWORD_GRANT, AUTH0_CRU_RESTAURANTS_SCOPE)
auth_header_cru_restaurants = {'authorization': 'Bearer ' + access_token_cru_restaurants}

# The following access token includes all four crud permissions, especially including delete.
access_token_del_restaurants = get_auth0_access_token(AUTH0_CLIENT_CRED_GRANT)
auth_header_del_restaurants = {'authorization': 'Bearer ' + access_token_del_restaurants}


if __name__ == '__main__':
    access_token = get_auth0_access_token()
    print(access_token)
