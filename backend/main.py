import os
import time
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

conn = get_db_connection()
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS visits (id serial PRIMARY KEY, ts timestamp DEFAULT CURRENT_TIMESTAMP);')
conn.commit()
cur.close()
conn.close()

@app.route('/')
def hello():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO visits (ts) VALUES (NOW());')
    cur.execute('SELECT COUNT(*) FROM visits;')
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Hello from Flask!", "visits_count": count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
