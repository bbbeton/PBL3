import serial
from time import sleep

agsm = serial.Serial("/dev/ttyS0", baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=8, timeout=1)


PIN = "2807"
Numbers = ["882183177", "664047400", "502495937", "512429025", "662275869", "504440436"]
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
        sleep(5)
        

if not agsm.inWaiting():
    write("AT+CPIN?")
    received_data = ''
sleep(1)
if agsm.inWaiting():
    received_data += read()
    print("AT+CPIN?\n")
    print(received_data+"\n")
    if received_data.find("SIM PIN") >= 0:
        write("AT+CPIN="+PIN)
        print("AT+CPIN="+PIN+"\n")
        sleep(1)
        print(read()+"\n")
write("AT+CMGF=1")
print("AT+CMGF=1\n")
sleep(1)
print(read()+"\n")
write("AT+CPBS=\"SM\"")
print("AT+CPBS=\"SM\"\n")
sleep(1)
print(read()+"\n")

sendSMS(Numbers,"test message")