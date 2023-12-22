from flask import Flask, jsonify, request
from time import sleep
import serial
import os

if not os.getuid() == 0:
    print("please use root privileges! try: \"sudo python new_server.py\"")
    exit(0)

agsm = serial.Serial("/dev/ttyS0", baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)


PIN = "1234"
phoneNumbers = ["664047400", "535666100", "502495937"]
MAX_TEMPERATURE = 30


def write(string):
    agsm.write((string+"\r\n").encode())
    
def read():
    return (agsm.read(agsm.inWaiting())).decode()
    
def sendSMS(phoneNumbers, message):
    for i in phoneNumbers:
        write(f'AT+CMGS=\"{i}\"')
        individual_message = message + chr(0x1A)
        write(individual_message)
        sleep(1)
        

if not agsm.inWaiting():
    write("AT+CPIN?")
    received_data = ''
sleep(0.1)
if agsm.inWaiting():
    received_data += read()
    print("AT+CPIN?\n")
    print(received_data+"\n")
    if received_data.find("SIM PIN") >= 0:
        write("AT+CPIN="+PIN)
        print("AT+CPIN="+PIN+"\n")
        sleep(0.1)
        print(read()+"\n")
write("AT+CMGF=1")
print("AT+CMGF=1\n")
sleep(0.1)
print(read()+"\n")
write("AT+CPBS=\"SM\"")
print("AT+CPBS=\"SM\"\n")
sleep(0.1)
print(read()+"\n")
# ~ write("AT+CNMI=2,0,0,0,0")
# ~ print("AT+CNMI=2,0,0,0,0\n")
# ~ sleep(0.1)
# ~ print(read()+"\n")
        

app = Flask(__name__)

data = [{'temperature': 25, 'smoke': 0},{'temperature': 25, 'smoke': 0}]

@app.route('/s/<int:id>', methods=['GET'])
def get_temperature(id):
    return jsonify({'temperature': data[id].get(temperature), 'smoke': data[id].get(smoke)})

@app.route('/s/<int:id>', methods=['PUT'])
def set_temperature(id):
    global data
    new_data = request.json
    if 'temperature' in new_data and 'smoke' in new_data:
        data[id].get(temperature) = new_data['temperature']
        data[id].get(smoke) = new_data['smoke']
        if data[id].get(temperature) >= MAX_TEMPERATURE:
            message = "Max shieldbox temperature exceeded!"
            sendSMS(phoneNumbers, message)
        elif data[id].get(smoke):
            message = "Smoke detected in your shieldbox!"
            sendSMS(phoneNumbers, message)
        return jsonify({'message': f"Temperature updated to {data[id].get(temperature)} and smoke updated to {data[id].get(smoke)}"})
    else:
        return jsonify({'error': 'Invalid JSON format or missing keys'})
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
