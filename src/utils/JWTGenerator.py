from joserfc.jwk import KeySet
from joserfc.jwt import JWTClaimsRegistry
from joserfc import jwt
from joserfc.errors import BadSignatureError, ExpiredTokenError, InvalidClaimError 
import json
import datetime
import base64

from src.utils.db_user import db_user

class JWTGen:
  def encode_jwt(email, uuid, request = 'email'):
    with open('oct-256.json', 'r') as f:
      data = json.load(f)
      key_set = KeySet.import_key_set(data)
    header = {'alg': "HS256"}
    payload = {"email": email, "uuid": uuid, "exp": int(datetime.datetime.now().timestamp() + 86400), "req": request, "iss": "gamescout"}
    if request is 'password': 
      payload['exp'] = int(datetime.datetime.now().timestamp() + 1800)
      modify_date = db_user.get_password_modified(email)
      payload['nonce'] = base64.b64encode(modify_date.encode("ascii")).decode("ascii")
    return jwt.encode(header, payload, key_set)
  def decode_jwt(token, e):
    with open('oct-256.json', 'r') as f:
      data = json.load(f)
      key_set = KeySet.import_key_set(data)

    s = jwt.decode(token, key_set) 
    claims_request = JWTClaimsRegistry(
      email={"essential": True, 'value': e, 'allow_blank': False},
      uuid={"essential": True, 'allow_blank': False},
      iss={"essential": True, 'allow_blank': False, 'value': "gamescout"}
    )
    try:
      claims_request.validate(s.claims)
    except (BadSignatureError, ExpiredTokenError, InvalidClaimError):
      return False
    return s.claims
  def generate_key():
    with open('oct-256.json', 'w') as f:
      f.write(json.dumps(KeySet.generate_key_set("oct", 256).as_dict()))