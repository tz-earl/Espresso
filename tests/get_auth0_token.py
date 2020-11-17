import http.client
import json

# Move these two credentials to environment variables.
AUTHO_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AUTHO_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


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
