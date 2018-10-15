import os
import io
import string
import random

import json
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import datetime

from flask import Flask, g, flash, send_file, render_template, url_for, abort, jsonify, redirect, request, make_response, session
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

    #Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    with db.get_db_cursor(commit=True) as cur:
            # cur.execute("""IF EXISTS (SELECT * FROM register where user_id=%s) BEGIN END 
            # ELSE BEGIN insert into register (name,user_id,avator) values (%s,%s,%s) END;""",(session.get('profile').get('user_id'),userinfo['name'],userinfo['sub'],userinfo['picture']))
            cur.execute("INSERT INTO register (user_id,name,avator) values (%s,%s,%s) ON CONFLICT (user_id) DO NOTHING;",(userinfo['sub'],userinfo['name'],userinfo['picture']))
            # user_id_res=[record["user_id"] for record in cur]
            # if  user_id_res==session.get('profile').get('user_id'):
            #     return redirect('/')
            # else :
            #cur.execute("""insert into register (name,user_id,avator) values (%s,%s,%s)""", (userinfo['name'],userinfo['sub'],userinfo['picture']))
    return redirect('/')

# Auth0 Login
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.environ['AUTH0_CALLBACK_URL'], audience='https://' + os.environ['AUTH0_DOMAIN']+'/userinfo')

# Auth0 Logout
@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID']}
    app.logger.info(auth0.api_base_url + '/v2/logout?' + urlencode(params))
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# Profile Page
@app.route('/profile')
@requires_auth
def profile():
#     with db.get_db_cursor() as cur:

#             cur.execute("""select  name,email from register where id=%s;""",userinfo['sub']  )

            
#             usr_name=[record["name"] for record in cur]
#             usr_email=[record["email"] for record in cur]
            
    return render_template('profile.html',usr_name=session.get('profile').get('name'),avator=session.get('profile').get('picture'))
@app.route('/user/<int:user_id>')
# @requires_auth
def show_post(user_id):
    # show the post with the given id, the id is an integer

    # TODO:next mileStone change status value to see which status of post the page is rendering

    # need data name email avator id, all information for the post for this user
    return render_template("profile.html")

# upload imaage into data base
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ['png', 'jpg']


# TODO For BATU, create upload to handle our form in profile html
@app.route('/upload', methods=['POST'])
def upload():
    title_res = request.form.get("title")
    status_res = request.form.get("status")
    location_res = request.form.get("location")
    budget_res = request.form.get("budget")
    text_res = request.form.get("text")
    dt = datetime.now()
    
    
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
            cur.execute("SELECT * FROM register where user_id=%s;",(session.get('profile').get('user_id'),))
            user_id_res=[record["id"] for record in cur]
            cur.execute("insert into post (publisher_id,time,title, status,location,budget,content) values (%s,%s,%s,%s,%s,%s, %s)",
                (user_id_res[0],dt, title_res, status_res,location_res,budget_res,text_res))
            cur.execute("SELECT MAX(post_id) AS maxid FROM post where publisher_id=%s;",(user_id_res[0],))
            post_id_res=[record["maxid"] for record in cur]
            cur.execute("insert into picture (register_id,post_id,img) values (%s,%s,%s)",
                (user_id_res[0], post_id_res, data))
            
    return redirect(url_for("profile"))

@app.route('/img/<int:img_id>')
def serve_img(img_id):
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM images where img_id=%s", (img_id,))
        image_row = cur.fetchone()

        # in memory binary stream
        stream = io.BytesIO(image_row["img"])

        return send_file(
            stream,
            attachment_filename=image_row["filename"])

if __name__ == '__main__':
    app.run()
