import os

from flask import Flask, g, render_template, url_for
import psycopg2

app = Flask(__name__)

# def connect_db():
#     """Connects to the specific database."""
#     return psycopg2.connect(os.environ.get('DB_DSN'))
#
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'pg_db'):
#         g.pg_db = connect_db()
#     return g.pg_db

# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'db'):
#         g.pg_db.close()

@app.route('/')
def home():
    return render_template("home.html")


# Auth0 Login
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback', audience=os.environ['AUTH0_DOMAIN']+'/userinfo')

# Auth0 Logout
@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': os.environ['CLIENT_ID']}
    app.logger.info(auth0.api_base_url + '/v2/logout?' + urlencode(params))
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))





if __name__ == '__main__':
    app.run()
