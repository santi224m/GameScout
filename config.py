import os

import redis

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'R0jPUc4gTiUAuy0S16fDFQuHiINo6brM'
    # Configure redis for flask-session
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url('redis://localhost:6379')
