from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Database Setup
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()


@app.route('/')
def home():
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (username, hashed)
            )
            conn.commit()
            return redirect('/login')

        except:
            return "User already exists"

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user[0]
        ):
            session['user'] = username
            return redirect('/dashboard')

        return "Invalid Credentials"

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if 'user' in session:
        return render_template(
            'dashboard.html',
            username=session['user']
        )

    return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)