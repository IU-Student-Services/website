import os
from flask import Flask
from authlib.integrations.flask_client import OAuth
from config import client_id, client_secret, redirect_uri, authorize_url, token_url, scope, secret_key

app = Flask(__name__)
app.secret_key = secret_key

oauth = OAuth(app)
oauth.register(
    name='cilogon',
    client_id=client_id,
    client_secret=client_secret,
    authorize_url=authorize_url,
    authorize_params=None,
    access_token_url=token_url,
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=redirect_uri,
    client_kwargs={'scope': ' '.join(scope)},
    jwks_uri='https://cilogon.org/oauth2/certs'
)

from app import routes