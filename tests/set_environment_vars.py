import os
# import json
from dotenv import load_dotenv, find_dotenv

# import unittest
#
# import get_auth0_token
# from get_auth0_token import get_auth0_access_token
# from get_auth0_token import AUTH0_PASSWORD_GRANT
# from get_auth0_token import AUTH0_CLIENT_CRED_GRANT
# from get_auth0_token import AUTH0_CRU_RESTAURANTS_SCOPE
#
# # Get the Auth0 access token just once to avoid repeated hits to the Auth0 API
# # "cru" means permissions to create-read-update
# access_token_cru_restaurants = get_auth0_access_token(AUTH0_PASSWORD_GRANT, AUTH0_CRU_RESTAURANTS_SCOPE)
# auth_header_cru_restaurants = {'authorization': 'Bearer ' + access_token_cru_restaurants}
#
# # The following access token includes all four crud permissions, especially including delete.
# access_token_del_restaurants = get_auth0_access_token(AUTH0_CLIENT_CRED_GRANT)
# auth_header_del_restaurants = {'authorization': 'Bearer ' + access_token_del_restaurants}


def set_environment_vars():
    """Set the env vars to have values for testing,
    in particular for the test database
    """
    ENV_FILE = find_dotenv()
    if ENV_FILE:
        load_dotenv(ENV_FILE)

    # Note that this testing apparently runs in its own environment,
    # so there is no need to save and restore env variables.
    try:
        os.environ['ESPRESSO_DB_USER'] = os.environ['ESPRESSO_TEST_DB_USER']
        os.environ['ESPRESSO_DB_PASSWORD'] = os.environ['ESPRESSO_TEST_DB_PASSWORD']
        os.environ['ESPRESSO_DB_HOST'] = os.environ['ESPRESSO_TEST_DB_HOST']
        os.environ['ESPRESSO_DB_DATABASE_NAME'] = os.environ['ESPRESSO_TEST_DB_DATABASE_NAME']
    except KeyError as ex:
        print("\nTesting requires four environment variables: " \
              "ESPRESSO_TEST_DB_USER  ESPRESSO_TEST_DB_PASSWORD  "
              "ESPRESSO_TEST_DB_HOST  ESPRESSO_TEST_DB_DATABASE_NAME")
        print(f"Environment variable {ex.args[0]} is missing")
        print(f"Please set {ex.args[0]} and restart the testing\n")
        raise
