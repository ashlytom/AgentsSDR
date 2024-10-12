from crewai_tools import BaseTool
import requests

class Listener(BaseTool):
    name: str = "Listener Agent"
    description: str = "Listen to APIs that track vehicle telemetry data."
    threshold: int = 40000

    def _run(self, threshold: int) -> str:
        try:
            # Make a GET request to the API endpoint
            response = requests.get('http://127.0.0.1:5000/vehicles')
            # Check if the request was successful
            if response.status_code == 200:
                vehicles = response.json()
                # Filter and collect vehicle numbers and UINs based on the threshold
                filtered_vehicles = [
                    (vehicle_number,kms_driven, uin) for vehicle_number, kms_driven, uin in vehicles if kms_driven > self.threshold
                ]
                # Format the result as a string
                result = "\n".join([f"Vehicle Number: {vn},Kilometers:{kms}, UIN: {uin}" for vn, kms, uin in filtered_vehicles])
                return result if result else "No vehicles exceed the threshold."
            else:
                return f"Failed to fetch data. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

#testing the tool   
# listener = Listener()
# result = listener._run(threshold=40000)
# print(result)