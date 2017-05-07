import os
import json
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash
from flask_mail import Mail, Message

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskapp.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskapp.db'),
    SECRET_KEY='key',
    USERNAME='admin',
    PASSWORD='pass',
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='username@gmail.com',  # tbc
    MAIL_PASSWORD='password'  # tbc
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

mail = Mail(app)


def connect_db():
    # Connect to the db
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    # Initialize the db
    init_db()
    print('Initialized the database.')


def get_db():
    # Connect to db if not connected already
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    # Close the db conn
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():

    search_text = request.args.get('text', default=None, type=str)
    flag = request.args.get('triggered', default=0, type=int)
    db = get_db()

    if search_text and search_text.strip() != "":
        s = '%{}%'.format(search_text)
        cur = db.execute("select title, text from entries where title like ? or text like ?", (s, s,))
    else:
        cur = db.execute('select title, text from entries order by id desc')

    entries = cur.fetchall()

    if not search_text and not flag:
        return render_template('show_entries.html', entries=entries)

    return json.dumps(dict(result=[dict(r) for r in entries]))


@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
                   [request.form["title"], request.form["text"]],)
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    return render_template('add_entry.html', error=None)


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        db = get_db()
        db.execute('insert into feedback (name, surname, email, subject, text) values (?, ?, ?, ?, ?)',
                   [request.form['name'], request.form['surname'], request.form['email'],
                    request.form['subject'], request.form['text']],)
        db.commit()

        # Send feedback as mail
        subject = "%s from %s %s" % (request.form['subject'], request.form['name'], request.form['surname'])
        msg = Message(subject,
                      sender=request.form['email'],
                      recipients=["sarikaya.duygu@gmail.com"])
        msg.body = request.form['text']
        # mail.send(msg) # uncomment if needed

        flash('Feedback was successfully sent')
        return redirect(url_for('show_entries'))

    return render_template('contact_us.html', error=None)

if __name__ == "__main__":
    app.run()
