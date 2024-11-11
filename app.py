from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database connection
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, name TEXT, offer TEXT, need TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Route for the form page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    offer = request.form.get('offer')
    need = request.form.get('need')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, offer, need) VALUES (?, ?, ?)", (name, offer, need))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Data submitted successfully"})

# Route to retrieve leaderboard data
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
