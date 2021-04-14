import http.client
import json
import os
from dotenv import load_dotenv, find_dotenv

# Get the AUTHO_CLIENT_ID and AUTHO_CLIENT_SECRET credentials.
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']

AUTH0_BARISTA_TEST_USER_NAME = os.environ['AUTH0_BARISTA_TEST_USER_NAME']
AUTH0_BARISTA_TEST_USER_PASSWORD = os.environ['AUTH0_BARISTA_TEST_USER_PASSWORD']

AUTH0_TASTER_TEST_USER_NAME = os.environ['AUTH0_TASTER_TEST_USER_NAME']
AUTH0_TASTER_TEST_USER_PASSWORD = os.environ['AUTH0_TASTER_TEST_USER_PASSWORD']

AUTH0_PASSWORD_GRANT = 'password'
AUTH0_CLIENT_CRED_GRANT = 'client_credentials'

AUTH0_CRU_RESTAURANTS_SCOPE = "read:restaurants create:restaurants update:restaurants"
AUTH0_CRUD_REVIEWS_SCOPE = "read:reviews create:reviews update:reviews delete:reviews"


def get_auth0_access_token(grant_type, scope=None, user=None, passwd=None):
    """Retrieves an access token using either (1) the Resource Owner Password Flow,
    documented at https://auth0.com/docs/flows/resource-owner-password-flow, or
    (2) the Auth0 Client Credentials Flow documented at
    https://auth0.com/docs/flows/client-credentials-flow and at
    https://auth0.com/docs/api/authentication#client-credentials-flow
    """
    conn = http.client.HTTPSConnection("espresso-dev.us.auth0.com")

    request_items = { "client_id": AUTH0_CLIENT_ID, \
                      "client_secret": AUTH0_CLIENT_SECRET, \
                      "audience": "api.espresso.routinew.com", \
                      "grant_type": grant_type
                     }
    if grant_type == AUTH0_PASSWORD_GRANT:
        request_items.update({ "username": user, \
                               "password": passwd, \
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


def get_auth0_access_barista():
    return get_auth0_access_token(AUTH0_PASSWORD_GRANT, AUTH0_CRU_RESTAURANTS_SCOPE,
                                  AUTH0_BARISTA_TEST_USER_NAME, AUTH0_BARISTA_TEST_USER_PASSWORD)

def get_auth0_access_taster():
    return get_auth0_access_token(AUTH0_PASSWORD_GRANT, AUTH0_CRUD_REVIEWS_SCOPE,
                                  AUTH0_TASTER_TEST_USER_NAME, AUTH0_TASTER_TEST_USER_PASSWORD)

# Get the Auth0 access tokens just once to avoid repeated hits to the Auth0 API

# The following access token includes create-read-update restaurant permissions.
access_token_cru_restaurants = get_auth0_access_barista()
auth_header_cru_restaurants = {'authorization': 'Bearer ' + access_token_cru_restaurants}

# The following access token includes all crud review permissions.
access_token_crud_reviews = get_auth0_access_taster()
auth_header_crud_reviews = {'authorization': 'Bearer ' + access_token_crud_reviews}

# The following access token includes all permissions.
access_token_all_permissions = get_auth0_access_token(AUTH0_CLIENT_CRED_GRANT)
auth_header_all_permissions = {'authorization': 'Bearer ' + access_token_all_permissions}

# For debugging
if __name__ == '__main__':
    access_token_barista = get_auth0_access_barista()
    print('\n BARISTA: ', access_token_barista)
    access_token_taster = get_auth0_access_taster()
    print('\n TASTER: ', access_token_taster)
