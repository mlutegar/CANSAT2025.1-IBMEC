import serial
import time

arduino = serial.Serial('COM12', 9600, timeout=1)
time.sleep(2)

with open('dados_arduino.txt', 'a') as file:
    while True:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            file.write(data + '\n')
            print(f'Dado recebido: {data}')
