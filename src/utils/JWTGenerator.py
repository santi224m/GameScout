from joserfc.jwk import KeySet
from joserfc.jwt import JWTClaimsRegistry
from joserfc import jwt
from joserfc.errors import BadSignatureError, ExpiredTokenError, InvalidClaimError 
import json
import datetime

class JWTGen:
  def encode_jwt(email, uuid):
    with open('oct-256.json', 'r') as f:
      data = json.load(f)
      key_set = KeySet.import_key_set(data)
    header = {'alg': "HS256"}
    payload = {"email": email, "uuid": uuid, "exp": int(datetime.datetime.now().timestamp() + 86400)}
    return jwt.encode(header, payload, key_set)
  def decode_jwt(token, e):
    with open('oct-256.json', 'r') as f:
      data = json.load(f)
      key_set = KeySet.import_key_set(data)

    s = jwt.decode(token, key_set) 
    claims_request = JWTClaimsRegistry(
      email={"essential": True, 'value': e, 'allow_blank': False},
      uuid={"essential": True, 'allow_blank': False}
    )
    try:
      claims_request.validate(s.claims)
    except (BadSignatureError, ExpiredTokenError, InvalidClaimError):
      return False
    return s.claims
  def generate_key():
    with open('oct-256.json', 'w') as f:
      f.write(json.dumps(KeySet.generate_key_set("oct", 256).as_dict()))