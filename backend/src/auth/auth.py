from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
# from dotenv import load_dotenv

import json, os

# load_dotenv()

AUTH0_DOMAIN = 'udacity-kaffee-shop.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'kaffe-shop'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
Obtains the Access Token from the Authorization Header
'''
def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise AuthError({
            "code": "missing_header",
            "description": "Expecting authorization header"
        }, 401)
    auth_header_parts = auth_header.split(" ")
    if auth_header_parts[0].lower() != "bearer":
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401) 
    elif len(auth_header_parts) == 1:
        raise AuthError({
            "code": "invalid_auth_header",
            "description": "Token not found. Expecting authorization header to be in the format --'Bearer token'"
         }, 401)
    elif len(auth_header_parts) > 2:
        raise AuthError({
            "code": "invalid_auth_header",
            "description": "Expecting authorization header to be in the format --'Bearer token'"
         }, 401)
    token = auth_header_parts[1]
    return token
    


'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    - Raises an AuthError if permissions are not included in the payload
    - Raise an AuthError if the requested permission string is not in the payload permissions array
    
    returns true otherwise
'''
def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError({
            "code": "invalid_claims",
            "description": "Permissions not included in JWT"
        })
    if permission not in payload["permissions"]:
        raise AuthError({
            "code": "unauthorized",
            "description": "Permission not found!"
        }, 403)
    return True

'''
    @INPUTS
        token: a json web token (string)
    returns the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except:
        raise AuthError({
            "code": "cannot_decode_token",
            "description": "Error decoding token headers."
        }, 401)

    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer='https://' + AUTH0_DOMAIN + '/')
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'expired_token',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)

    

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator