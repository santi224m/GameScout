from flask import request, redirect, url_for, session
from src.verify import bp

from src.utils.db_user import db_user

@bp.route('/', methods=('GET', 'POST'))
def verify():
  if session['user']['uuid'] and "id" in request.args:
    status = db_user.verify_user(request.args['id'])
    if "already-verified" in status: print("User already verified")
    elif "verified" in status: print("User is now verified")
    return redirect(url_for("main.index"))
  else: return redirect(url_for("main.index"))
  
