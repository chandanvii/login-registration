from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'app_user',
    'password': 'Skycap@19',
    'host': '192.168.1.11',
    'database': 'login_app'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return 'Login successful'
        else:
            return 'Invalid credentials'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

