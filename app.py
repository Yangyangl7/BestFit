import os
import string
import random

import json
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode
from functools import wraps

from flask import Flask, g, render_template, url_for, abort, jsonify, redirect, request, make_response, session
import psycopg2

import db
import auth

app = Flask(__name__)

def id_generator(size=13, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

@app.before_first_request
def initialize():
    db.setup()
    auth.setup()
    global auth0
    auth0 = auth.auth0

# Protected Page. Only accessible after login
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

# uncomment following 3 lines when 404 page has been created.
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("404.html"), 404

@app.route('/')
def home():
    return render_template("home.html")

# Auth0 callback after login
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')

# Profile Page
@app.route('/profile')
@requires_auth
def profile():
    return render_template('profile.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

# Auth0 Login
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.environ['AUTH0_CALLBACK_URL'], audience=os.environ['AUTH0_DOMAIN']+'/userinfo')

# Auth0 Logout
@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID']}
    app.logger.info(auth0.api_base_url + '/v2/logout?' + urlencode(params))
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/user/<int:user_id>')
# @requires_auth
def show_post(user_id):
    # show the post with the given id, the id is an integer
    # sql

    # name email avator id, post lists
    return render_template("profile.html")

# upload imaage into data base
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['png', 'jpg']

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash("no file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("no selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # convert the flask object to a regular file object
        data = request.files['file'].read()

        with db.get_db_cursor(commit=True) as cur:
            # we are storing the original filename for demo purposes
            # might be useful to also/instead save the file extension or mime type
            cur.execute("insert into images (filename, img) values (%s, %s)",
                (filename, data))
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run()
