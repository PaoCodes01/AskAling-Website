from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Math22413')
DB_PATH = 'contacts.db'

app = Flask(__name__)
CORS(app)

# Ensure DB and table exist
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    email TEXT,
    phone TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()

@app.route('/api/contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    required = ['firstName', 'lastName', 'email', 'phone', 'message']
    if not all(k in data and data[k] for k in required):
        return jsonify({'error': 'All fields required.'}), 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO contacts (firstName, lastName, email, phone, message) VALUES (?, ?, ?, ?, ?)''',
              (data['firstName'], data['lastName'], data['email'], data['phone'], data['message']))
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 200

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    admin_password = request.args.get('admin_password')
    if admin_password != ADMIN_PASSWORD:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM contacts ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    contacts = [
        {
            'id': row[0],
            'firstName': row[1],
            'lastName': row[2],
            'email': row[3],
            'phone': row[4],
            'message': row[5],
            'created_at': row[6]
        } for row in rows
    ]
    return jsonify(contacts)

if __name__ == '__main__':
    app.run(debug=True)
