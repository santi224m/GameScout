from flask import redirect, url_for, session
from src.verify import bp

from src.utils.db_user import db_user
from src.utils.JWTGenerator import JWTGen

@bp.route('/<jwt>')
def verify(jwt):
  if "user" in session and jwt:
    claims = JWTGen.decode_jwt(jwt, session['user']['email'])
    if not claims or session['user']['email'] != claims['email']: return redirect(url_for("main.index"))
    if db_user.verify_user(claims['uuid']): print("User is now verified")
    else: print("User already verified")
  elif jwt: 
    session["redirect"] = "verify.verify"
    session["jwt"] = jwt
    return redirect(url_for("signin.signin"))
  return redirect(url_for("main.index"))
  
