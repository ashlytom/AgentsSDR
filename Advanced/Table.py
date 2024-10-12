import sqlite3
import random
import time
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_number TEXT,
            kms_driven INTEGER,
            uin TEXT
        )
    ''')
    # Insert sample data
    vehicles = [
        ('ABC123', 10000, 'UIN001'),
        ('DEF456', 15000, 'UIN002'),
        ('GHI789', 20000, 'UIN003'),
        ('JKL012', 25000, 'UIN004'),
        ('MNO345', 30000, 'UIN005'),
        ('PQR678', 35000, 'UIN006'),
        ('STU901', 40000, 'UIN007'),
        ('VWX234', 45000, 'UIN008'),
        ('YZA567', 50000, 'UIN009'),
        ('BCD890', 55000, 'UIN010')
    ]
    cursor.executemany('INSERT INTO vehicles (vehicle_number, kms_driven, uin) VALUES (?, ?, ?)', vehicles)
    conn.commit()
    conn.close()

# Increment odometer values
def increment_odometer():
    while True:
        conn = sqlite3.connect('vehicles.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, kms_driven FROM vehicles')
        vehicles = cursor.fetchall()
        for vehicle in vehicles:
            delta = random.randint(1, 10)  # Random delta
            new_kms = vehicle[1] + delta
            cursor.execute('UPDATE vehicles SET kms_driven = ? WHERE id = ?', (new_kms, vehicle[0]))
        conn.commit()
        conn.close()
        time.sleep(5)  # Wait for 5 seconds before next increment

# API endpoint to get vehicle data
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    conn = sqlite3.connect('vehicles.db')
    cursor = conn.cursor()
    cursor.execute('SELECT vehicle_number, kms_driven, uin FROM vehicles')
    vehicles = cursor.fetchall()
    conn.close()
    return jsonify(vehicles)

if __name__ == '__main__':
    init_db()
    # Start the odometer increment loop in a separate thread
    from threading import Thread
    Thread(target=increment_odometer, daemon=True).start()
    # Run the Flask app
    app.run(debug=True, port=5000)