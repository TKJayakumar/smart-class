from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'temporary_key'

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='clonedb.c7kcawq6wjvr.eu-north-1.rds.amazonaws.comt',
        user='admin',
        password='Onlineawsnm',
        database='clone_db'
    )

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Example course URLs (you can replace these with real links from a database or S3)
    course_urls = [
        "https://clonebuckeet.s3.eu-north-1.amazonaws.com/java_tutorial.pdf",
        "https://clonebuckeet.s3.eu-north-1.amazonaws.com/mementopython3-english.pdf",
    ]
    return render_template('dashboard.html', course_urls=course_urls)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
