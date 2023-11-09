from flask import render_template, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
from app import app, oauth, redirect_uri
import os

@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login')
def login():
    # Generate a nonce and store it in the session
    nonce = os.urandom(16).hex()
    session['oauth_nonce'] = nonce

    return oauth.cilogon.authorize_redirect(
        redirect_uri=redirect_uri,
        nonce=nonce  # Pass the nonce to the authorize_redirect
    )

@app.route('/callback')
def callback():
    token = oauth.cilogon.authorize_access_token()
    nonce = session.pop('oauth_nonce', None)
    user_info = oauth.cilogon.parse_id_token(token, nonce=nonce)
    session['user_info'] = user_info
    return redirect(url_for('authenticated'))


@app.route('/authenticated')
def authenticated():
    user_info = session.get('user_info')
    if user_info:
        return f'User: {user_info}, <a href="/logout">Logout</a>'
    else:
        return 'Not authenticated. <a href="/login">Login with CILogon</a>'


@app.route('/logout')
def logout():
    session.pop('user_info', None)
    return 'Logged out. <a href="/">Back to Home</a>'