import socket
import threading
import json
import os
import cv2
import numpy as np
import struct
from io import BytesIO



def enter_server():
    os.system('cls||clear')
    with open('servers.json') as f:
        data = json.load(f)
    print('Your servers: ', end="")
    for servers in data:
        print(servers, end=" ")
    server_name = input("\nEnter the server name:")
    global nickname
    global password
    nickname = input("Choose Your Nickname:")
    if nickname == 'admin':
        password = input("Enter Password for Admin:")

    ip = data[server_name]["ip"]
    port = data[server_name]["port"]
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.setblocking(False)
    client.send(nickname.encode('ascii'))
            


def add_server():
    os.system('cls||clear')
    server_name = input("Enter a name for the server:")
    server_ip = input("Enter the ip address of the server:")
    server_port = int(input("Enter the port number of the server:"))

    with open('servers.json', 'r') as f:
        data = json.load(f)
    with open('servers.json', 'w') as f:
        data[server_name] = {"ip": server_ip, "port": server_port}
        json.dump(data, f, indent=4)


while True:
    os.system('cls||clear')
    option = input("(1)Enter server\n(2)Add server\n")
    if option == '1':
        enter_server()
        break
    elif option == '2':
        add_server()

stop_thread = False


msg = True
cap = cv2.VideoCapture(0)
def write():
    global msg
    while msg != 'None':
        if stop_thread:
            break

        try:
            ret, frame = cap.read()
            if frame is not None:
                memfile = BytesIO()
                np.save(memfile, frame)
                memfile.seek(0)
                data = memfile.read()
                client.sendall(struct.pack("L", len(data)) + data)
            else:
                print('Retry')
        except Exception:
            # print('Error')
            client.sendall(struct.pack("L", len(data)) + data)
    # msg = client.recv(1024).decode('ascii')



write_thread = threading.Thread(target=write)
write_thread.start()
