import requests
import json

API_URL = "http://192.168.114.70:8000/shieldbox/devices/1/sensors/Sensor"  # Replace with your actual API endpoint URL

def send_data(temperature, gas_state):
    data = {"name": "Sensor", "value": temperature, "smoke_value": gas_state}
    print(data)

    try:
        response = requests.put(API_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        print(response.status_code)
        if response.status_code == 200 and response.content:
            return response.json()
        else:
            print(f"Unexpected response: {response.status_code}, {response.content}")

    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")

# Example usage:
temperature_value = 25
gas_state_value = 0
send_data(temperature_value, gas_state_value)
