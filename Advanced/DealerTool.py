import requests
import json
from crewai_tools import BaseTool

class DealerTalker(BaseTool):
    name: str = "Dealer API Agent"
    description: str = "Talks to dealers and checks their date, and time slots with place."

    def _run(self) -> dict:
        # Read customer details from the text file
        try:
            with open('customer_details.txt', 'r') as file:
                lines = file.readlines()
                # Extract city, date, and time from the file
                city = lines[0].split(": ")[1].strip()
                date = lines[1].split(": ")[1].strip()
                time = lines[2].split(": ")[1].strip()
        except FileNotFoundError:
            print("Error: The file customer_details.txt was not found.")
            return {"error": "The file customer_details.txt was not found."}
        except Exception as e:
            print(f"Error: An error occurred while reading the file: {e}")
            return {"error": f"An error occurred while reading the file: {e}"}

        # Prepare the slot request
        slot_request = {
            "city": city,
            "date": date,
            "time": time
        }

        base_url = 'http://127.0.0.1:5002'
        try:
            # Send a GET request to the dealership slots endpoint
            response = requests.get(f'{base_url}/dealership-slots')
            
            # Check if the request was successful
            if response.status_code == 200:
                dealership_data = response.json()

                # Check if the requested slot is open or closed
                city_slots = dealership_data.get(slot_request["city"], [])
                slot_status = "closed"  # Default to closed if not found
                for date_info in city_slots:
                    if date_info["date"] == slot_request["date"]:
                        for slot in date_info["slots"]:
                            if slot["time"] == slot_request["time"]:
                                slot_status = slot["status"]
                                break

                # Save the result to a text file
                with open('slot_status.txt', 'w') as output_file:
                    output_file.write(f"Requested Slot Status: {slot_status}\n")

                return {"status": slot_status}
            else:
                print(f"Error: Failed to fetch dealership slots. Status code: {response.status_code}")
                return {"error": f"Failed to fetch dealership slots. Status code: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred: {e}")
            return {"error": f"An error occurred: {e}"}

# Testing the DealerTalker
# if __name__ == '__main__':
#     dealer_talker = DealerTalker()
#     result = dealer_talker._run()
#     print(json.dumps(result, indent=4))