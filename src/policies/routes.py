from flask import render_template
from src.policies import terms_bp, privacy_bp

@terms_bp.route('/', methods=['GET'])
def terms():
  return render_template('policies/terms.html')

@privacy_bp.route('/', methods=['GET'])
def privacy():
  return render_template('policies/privacy.html')