import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, 
                       name TEXT, 
                       offer TEXT, 
                       need TEXT, 
                       topics TEXT)''')
    conn.commit()
    conn.close()

# Run the function to create the table
init_db()
print("Database and table created successfully.")
