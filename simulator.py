import socket
import random
import time

count = 0
seq = []

IP = '127.0.0.1'
PORT = 25001

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def SendData(message):
    s.sendto(message.encode(), (IP, PORT))
    print(f"{message} sent")
    
while (True):
    count += 1
    
    # if count % 30 == 0:
    isMovement = random.randint(0, 1)
    
    
    direction = random.randint(0, 4)
    
    string = f"1, {direction}"
    
    SendData(string)
    
    time.sleep(0.5)