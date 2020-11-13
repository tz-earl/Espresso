"""Extracted from Python Flask API Auth0 integration example
"""


from functools import wraps
import json
from os import environ as env
from urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
from flask import request, _request_ctx_stack
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_IDENTIFIER = env.get("API_IDENTIFIER")
ALGORITHMS = ["RS256"]


# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"success": False,
                        "message":
                            "Authorization header is missing"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"success": False,
                        "description":
                            "Invalid header: "
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"success": False,
                        "description": "Invalid header: Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"success": False,
                        "description":
                            "Invalid header: "
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({"success": False,
                            "description":
                                "Invalid header: "
                                "Use an RS256 signed JWT Access Token"}, 401)
        if unverified_header["alg"] == "HS256":
            raise AuthError({"success": False,
                            "description":
                                "Invalid header: "
                                "Use an RS256 signed JWT Access Token"}, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"success": False,
                                "description": "Token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"success": False,
                                "description":
                                    "Invalid claims,"
                                    " please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"success": False,
                                "description":
                                    "Invalid header: "
                                     "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"success": False,
                        "description": "Invalid header: Unable to find appropriate key"}, 401)
    return decorated
