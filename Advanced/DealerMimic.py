from flask import Flask, jsonify
import random

app = Flask(__name__)

# Sample data for dealership service slots
def generate_service_slots():
    places = {
        "Mumbai": [
            {"date": "2023-12-01", "slots": [
                {"time": "09:00 AM - 11:00 AM", "status": "open"},
                {"time": "11:00 AM - 01:00 PM", "status": "closed"},
                {"time": "2:00 AM - 3:00 PM", "status": "open"}
            ]},
            {"date": "2023-12-02", "slots": [
                {"time": "09:00 AM - 11:00 AM", "status": random.choice(["open", "closed"])},
                {"time": "11:00 AM - 01:00 PM", "status": random.choice(["open", "closed"])}
            ]}
        ],
        "Delhi": [
            {"date": "2023-12-01", "slots": [
                {"time": "09:00 AM - 11:00 AM", "status": random.choice(["open", "closed"])},
                {"time": "11:00 AM - 01:00 PM", "status": random.choice(["open", "closed"])}
            ]},
            {"date": "2023-12-02", "slots": [
                {"time": "09:00 AM - 11:00 AM", "status": random.choice(["open", "closed"])},
                {"time": "11:00 AM - 01:00 PM", "status": random.choice(["open", "closed"])}
            ]}
        ],
        "Bangalore": [
            {"date": "2023-12-01", "slots": [
                {"time": "09:00 AM - 11:00 AM", "status": random.choice(["open", "closed"])},
                {"time": "11:00 AM - 01:00 PM", "status": random.choice(["open", "closed"])}
            ]},
            {"date": "2023-12-02", "slots": [
                {"time": "09:00 AM - 11:00 AM", "status": random.choice(["open", "closed"])},
                {"time": "11:00 AM - 01:00 PM", "status": random.choice(["open", "closed"])}
            ]}
        ]
    }
    return places

@app.route('/dealership-slots', methods=['GET'])
def get_dealership_slots():
    # Generate and return the service slot data
    service_slots = generate_service_slots()
    return jsonify(service_slots)

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # You can change the port if needed