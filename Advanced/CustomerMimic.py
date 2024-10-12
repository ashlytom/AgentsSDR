from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for locations, dates, and timeslots
service_data = {
    "locations": ["Mumbai"],
    "dates": ["2023-12-01"],
    "timeslots": ["09:00 AM - 11:00 AM"]
}

@app.route('/service-options', methods=['GET'])
def get_service_options():
    # Return the service data as JSON
    return jsonify(service_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # You can change the port if needed