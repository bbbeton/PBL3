import os
import glob
import time
import requests
import json
from django.http import JsonResponse
import RPi.GPIO as GPIO
from config import API_URL
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pin for reading the DO output
DO_PIN = 7  # Replace with the actual GPIO pin number
GPIO.setup(DO_PIN, GPIO.IN)

def send_data(temperature, gas_state):
    data = {"name": "Sensor", "value": temperature, "smoke_value": gas_state}
    print(data)
    response = requests.put(API_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(response.status_code)
    if response.status_code == 200 and response.content:
        return response.json()
    else:
        print(f"Unexpected response: {response.status_code}, {response.content}")



def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
	
def detect_gas():
    gas_present = GPIO.input(DO_PIN)
    if gas_present == GPIO.LOW:
        gas_state = 1
        
    else:
        gas_state = 0
    return gas_state


while True:
    temp_state = read_temp()
    gas_state = detect_gas()
    print(f"{gas_state}\nTemperature: {temp_state}")
    send_data(temp_state, gas_state)
    for i in range(10):
        gas_state = detect_gas()
        if gas_state == 1:
            print(f"{gas_state}\nTemperature: {temp_state}")
            send_data(temp_state, gas_state)
            time.sleep(10)
        time.sleep(0.1)