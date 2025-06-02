from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",  # Add your MySQL password
    database="franchise_management"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def LGMS():
    return render_template('LGMS.html')
@app.route('/')
def home():
    return '<h2>Welcome to Lead Generation App</h2><p><a href="/login">Login Here</a></p>'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form['email']
    password = request.form['password']
    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    if user:
        session['email'] = user['email']
        session['role'] = user['role']
        return redirect(f"/dashboard/{user['role']}")
    return render_template('login.html', error="Invalid credentials")

@app.route('/dashboard/<role>')
def dashboard(role):
    if session.get('role') == role:
        return render_template(f"dashboard_{role}.html")
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
