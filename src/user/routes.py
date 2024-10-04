import requests

from flask import Blueprint, render_template, request, abort
from src.user import user_bp, signup_bp

@user_bp.route('/', methods=('GET', 'POST'))
def user():
    return render_template('user/userpage.html')

@signup_bp.route('/', methods=('GET', 'POST'))
def signup():
    return render_template('user/sign_up.html')