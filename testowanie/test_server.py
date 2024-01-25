import asyncio
import time
import httpx
import csv 
import json

async def fetch(url, method='GET', headers=None, params=None, data=None):
    async with httpx.AsyncClient() as client:
        if method == 'GET':
            response = await client.get(url, headers=headers, params=params)
        elif method == 'PUT':
            response = await client.put(url, headers=headers, params=params, data=data)
        else:
            raise ValueError("Invalid HTTP method")

        return response

async def send_requests(url, num_requests, method='PUT', headers={'Content-Type': 'application/json'}, params=None, data=json.dumps({"name": "Sensor", "value": 17.5, "smoke_value": 0})):
    tasks = [fetch(url, method=method, headers=headers, params=params, data=data) for _ in range(num_requests)]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses

def extract_data(response):
    if isinstance(response, Exception):
        return {"name": "Request Failed", "value": str(response), "smoke_value": ""}
    else:
        return {"name": f"Request {response.request.method} {response.url}", "value": str(response.status_code), "smoke_value": str(response.elapsed.total_seconds())}

def print_results(responses):
    for i, response in enumerate(responses):
        data = extract_data(response)
        if isinstance(response, Exception):
            print(f"{data['name']}: Failed - {data['value']}")
        else:
            print(f"{data['name']}: Status Code - {data['value']}, Elapsed Time - {data['smoke_value']} seconds")

if __name__ == "__main__":
    url = "http://192.168.114.70:8000/shieldbox/devices/1/sensors/Sensor"
    num_requests = 10
    method = 'PUT'
    headers = {'Content-Type': 'application/json'}

    start_time = time.time()

    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(send_requests(url, num_requests, method=method, headers=headers))

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nTotal Elapsed Time: {total_time} seconds\n")
    csv_file_path = "test_results.csv"

    # ...

    with open(csv_file_path, mode='w', newline='') as file_output:
        csv_writer = csv.writer(file_output)
        csv_writer.writerow(["Status_code", "Elapsed_time"])  # Write header

        for response in responses:
            data = extract_data(response)
            csv_writer.writerow([data['value'], data['smoke_value']])


    print_results(responses)
