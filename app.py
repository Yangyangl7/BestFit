import os

from flask import Flask, g, render_template, url_for
import psycopg2

app = Flask(__name__)

def connect_db():
    """Connects to the specific database."""
    return psycopg2.connect(os.environ.get('DB_DSN'))

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'pg_db'):
        g.pg_db = connect_db()
    return g.pg_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.pg_db.close()

@app.route('/')
def home():
    return render_template("homepage.html")

@app.route('/user/<int:user_id>')
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
