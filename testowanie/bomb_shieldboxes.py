import asyncio
import httpx
import csv
import json
import random
from datetime import datetime

async def send_data(client, base_url, device_id):
    smoke_url = f"{base_url}/{device_id}/smoke/"
    temp_url = f"{base_url}/{device_id}/temp/"

    smoke_payload = {"smoke_value": random.choice([0.0, 1.0])}
    temp_payload = {"temp_value": round(random.uniform(25.0, 30.0), 2)}
    elapsed_time_prev = 0
    print(f"\nSending data to Device {device_id}")
    print(f"Smoke URL: {smoke_url}")
    print(f"Smoke Payload: {smoke_payload}")

    try:
        start_time = datetime.now().timestamp()
        smoke_response = await client.post(smoke_url, json=smoke_payload, timeout=10.0)
        temp_response = await client.post(temp_url, json=temp_payload, timeout=10.0)
        end_time = datetime.now().timestamp()

        elapsed_time = end_time - start_time - elapsed_time_prev

        elapsed_time_prev = elapsed_time

        print(f"Device {device_id} - Smoke POST: {smoke_response.status_code}")
        print(f"Device {device_id} - Temp POST: {temp_response.status_code}")
        print(f"Elapsed Time for Device {device_id}: {elapsed_time} seconds")

        return {"device_id": device_id, "smoke_status_code": smoke_response.status_code,
                "temp_status_code": temp_response.status_code, "elapsed_time": elapsed_time}
    except httpx.RequestError as e:
        print(f"Error for Device {device_id}: {e}")
        return {"device_id": device_id, "error": str(e), "elapsed_time": None}

async def simulate_shieldboxes(base_url, num_shieldboxes):
    async with httpx.AsyncClient() as client:
        tasks = [send_data(client, base_url, device_id) for device_id in range(1, num_shieldboxes + 1)]
        return await asyncio.gather(*tasks)

def save_to_csv(file_path, results):
    with open(file_path, mode='w', newline='') as file_output:
        csv_writer = csv.writer(file_output)
        csv_writer.writerow(["Device_ID", "Smoke_Status_Code", "Temp_Status_Code", "Elapsed_Time"])

        for result in results:
            device_id = result.get("device_id", "")
            smoke_status_code = result.get("smoke_status_code", "500")
            temp_status_code = result.get("temp_status_code", "500")
            elapsed_time = result.get("elapsed_time", "0")

            csv_writer.writerow([device_id, smoke_status_code, temp_status_code, elapsed_time])


if __name__ == "__main__":
    base_url = "http://192.168.0.94:8000/shieldboxes"
    num_shieldboxes = 500 # Specify the number of ShieldBoxes to simulate
    csv_file_path = f"test_results_{num_shieldboxes}_3.csv"

    loop = asyncio.get_event_loop()

    try:
        results = loop.run_until_complete(simulate_shieldboxes(base_url, num_shieldboxes))
        save_to_csv(csv_file_path, results)
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
