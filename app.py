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





if __name__ == '__main__':
    app.run()
