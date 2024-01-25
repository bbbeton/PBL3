import requests
import json
import random

def create_shieldboxes(base_url, num_shieldboxes):
    shieldboxes = []

    for box_id in range(3, num_shieldboxes + 3):
        shieldbox_data = {
            "name": f"ShieldBox{box_id}",
            "smoke_sensor": [],
            "temp_sensor": []
        }

        response = requests.post(f"{base_url}/shieldboxes/shieldbox/{box_id}/", json=shieldbox_data)

        print(f"Request URL: {base_url}/shieldboxes/{box_id}/")
        print(f"Request Payload: {json.dumps(shieldbox_data, indent=2)}")
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 201:
            shieldboxes.append(shieldbox_data)
            print(f"ShieldBox{box_id} created successfully.")
        else:
            print(f"Failed to create ShieldBox{box_id}. Status code: {response.status_code}")

    return shieldboxes

if __name__ == "__main__":
    base_url = "http://192.168.0.94:8000"
    num_shieldboxes = 1000  # Specify the number of ShieldBoxes to create

    created_shieldboxes = create_shieldboxes(base_url, num_shieldboxes)
    print("\nCreated ShieldBoxes:")
    print(json.dumps(created_shieldboxes, indent=2))
