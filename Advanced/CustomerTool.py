import requests
import json
import random
from crewai_tools import BaseTool

class CustomerTalker(BaseTool):
    name: str = "Customer API Agent"
    description: str = "Talks to customers and gets their preferred place, date, and time slots."

    def _run(self) -> dict:
        # Read vehicle data from the text file first
        vehicles = []
        try:
            with open('task1output.txt', 'r') as file:
                for line in file:
                    # Assuming each line is formatted as "Vehicle Number: ABC123, UIN: UIN001"
                    parts = line.strip().split(', ')
                    vehicle_number = parts[0].split(': ')[1]
                    uin = parts[1].split(': ')[1]
                    vehicles.append({"vehicle_number": vehicle_number, "uin": uin})
            
            # Choose one vehicle randomly
            if vehicles:
                chosen_vehicle = random.choice(vehicles)
                print(f"Chosen Vehicle: {chosen_vehicle['vehicle_number']}, UIN: {chosen_vehicle['uin']}")
            else:
                print("No vehicles found in the file.")
                return {"error": "No vehicles found in the file."}
        
        except FileNotFoundError:
            print("The file task1output.txt was not found.")
            return {"error": "The file task1output.txt was not found."}
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return {"error": f"An error occurred while reading the file: {e}"}

        # Proceed with fetching service options from the API
        base_url = 'http://127.0.0.1:5001'
        
        try:
            # Send a GET request to the service options endpoint
            response = requests.get(f'{base_url}/service-options')
            
            # Check if the request was successful
            if response.status_code == 200:
                service_data = response.json()
                # Save the JSON data locally
                with open('customer_details.txt', 'w') as f:
                    json.dump(service_data, f, indent=4)
                return service_data
            else:
                return {"error": f"Failed to fetch service options. Status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"An error occurred: {e}"}

# Testing the CustomerTalker
# if __name__ == '__main__':
#     customer_api = CustomerTalker()
#     result = customer_api._run()
#     print(json.dumps(result, indent=4))