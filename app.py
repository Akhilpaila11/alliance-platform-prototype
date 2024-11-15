from flask import Flask, render_template, request, jsonify
import sqlite3
import openai  # Assuming OpenAI API for topic suggestions (replace with a simple mock if not using OpenAI)

app = Flask(__name__)

# Initialize the database connection
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, name TEXT, offer TEXT, need TEXT, topics TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Submit user data
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    offer = request.form.get('offer')
    need = request.form.get('need')
    topics = request.form.get('topics')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Check if the entry already exists
    cursor.execute("SELECT * FROM users WHERE name = ? AND offer = ? AND topics = ?", (name, offer, topics))
    existing_entry = cursor.fetchone()

    if existing_entry:
        conn.close()
        return jsonify({"status": "failed", "message": "This entry already exists."})

    # Insert only if no existing entry is found
    cursor.execute("INSERT INTO users (name, offer, need, topics) VALUES (?, ?, ?, ?)", (name, offer, need, topics))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Data submitted successfully"})

# Fetch connections based on offer/need match
@app.route('/connections', methods=['GET'])
def connections():
    offer = request.args.get('offer')  # Allow filtering by offer if provided

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    if offer:
        cursor.execute("SELECT name, offer, topics FROM users WHERE need = ?", (offer,))
    else:
        cursor.execute("SELECT name, offer, topics FROM users")
    
    users = cursor.fetchall()
    conn.close()

    unique_users = list(set(users))
    return jsonify(unique_users)

# AI-based topic suggestions
@app.route('/suggestions', methods=['POST'])
def suggestions():
    topics = request.form.get('topics')
    
    # AI-based suggestion using OpenAI API (mock for demonstration)
    if topics:
        topic_list = topics.split(',')
        # Simple keyword matching as a placeholder for AI suggestions
        suggestions = [f"Discuss {topic.strip()} with others interested in {topic.strip()}" for topic in topic_list]
        return jsonify(suggestions)
    else:
        return jsonify({"error": "No topics provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)
