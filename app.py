from flask import Flask, request
import sqlite3

app = Flask(__name__)

db = sqlite3.connect(':memory:', check_same_thread=False)
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

cursor.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com')")
cursor.execute("INSERT INTO users (username, email) VALUES ('bob', 'bob@example.com')")
cursor.execute("INSERT INTO users (username, email) VALUES ('ali', 'ali@example.com')")
cursor.execute("INSERT INTO users (username, email) VALUES ('veli', 'veli@example.com')")
cursor.execute("INSERT INTO users (username, email) VALUES ('jack', 'jack@example.com')")
cursor.execute("INSERT INTO users (username, email) VALUES ('heidi', 'bob@example.com')")


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello/<username>')
def hello_user(username):
    return f'Welcome to your page, {username}!'

@app.route('/search')
def search():
    search_query = request.args.get('q', '')

    if search_query:
        return f'You searched for {search_query}'
    return 'Please enter search term'

@app.route('/lookup')
def lookup():
    target_user = request.args.get('username')
    if not target_user:
        return 'Please enter your username'
    
    cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (target_user,))
    user = cursor.fetchone()

    if user:
        return f"Found user -> ID: {user[0]}, Username: {user[1]}, Email: {user[2]}"
    else:
        return 'User not found'

@app.route('/lookup-unsafe')
def lookup_user_unsafe():
    target_user = request.args.get('username')

    if not target_user:
        return "Please provide a username, like: /lookup-unsafe?username=alice"
    
    query = f"SELECT id, username, email FROM users WHERE username = '{target_user}'"
    cursor.execute(query)
    users = cursor.fetchall()

    if users:
        result = "<h3>Users Found:</h3><ul>"
        for user in users:
            result += f"<li>ID: {user[0]}, Username: {user[1]}, Email: {user[2]}</li>"
        result += "</ul>"
        return result
    else:
        return "User not found!"