import socket
import threading
import json
import os
import struct
import cv2
import numpy as np
from io import BytesIO
import pickle
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

payload_size = struct.calcsize("L")

def receive():
    while True:
        # global stop_thread
        # if stop_thread:
        #     break
        try:
            data = client.recv(payload_size)    
            if data is not None:
                msg_size = struct.unpack("L", data)[0]
                data = b''
                while len(data) < msg_size:
                    missing_data = client.recv(msg_size - len(data))
                    if missing_data:
                        data += missing_data
                    else:
                        pass
                # print(data)
                memfile = BytesIO()
                memfile.write(data)
                memfile.seek(0)
                frames = np.load(memfile)
                # print('Working')
                # print(frames.shape)
                
                cv2.imshow('frame', frames)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                cv2.destroyAllWindows()
                break
            
        except socket.error:

            print('Error Occured while Connecting')
            # client.close()
            # break



receive_thread = threading.Thread(target=receive)
receive_thread.start()
