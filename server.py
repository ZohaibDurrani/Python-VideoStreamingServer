import threading
import socket
import struct
import cv2
import numpy as np
from io import BytesIO

host = "127.0.0.1"
port = 5555 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host, port))
payload_size = struct.calcsize("L")
server.listen()
# clients = []
connections = []
sockets_list = [server]
clients = {}

def broadcast(message):
    # for client in clients:
        print(message)
        # client.send(message)
 
def handle(client):
    while True:
        try:
            data = client.recv(payload_size)
            # print(data)
            if data:
                msg_size = struct.unpack("L", data)[0]
                # print(msg_size)
                data = b''
                while len(data) < msg_size:
                    missing_data = client.recv(msg_size - len(data))
                    if missing_data:
                        data += missing_data
                    else:
                        pass
                
                if '1' in clients and '2' in clients:
                    clients['2'].sendall(struct.pack("L", len(data)) + data)

                
                # if len(clients) > 1:
                #     clients[1].sendall(struct.pack("L", len(data)) + data)
                # else:
                #     index = client.index(client)

        except socket.error:
            if client in clients.values():
                print('Clossing connection')
                site = [c for c in clients if clients[c] == client][0]
                # client.shutdown(1)
                client.close()
                broadcast(f'{site} closed') 
                clients.pop(site)
                break

                # client.shutdown(1)
                # client.close()
                # conn = connections[index]
                # br+nections.remove(conn)
            


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        # global site
        site = client.recv(1024).decode('ascii')
        
        connections.append(site)
        # clients.append(client)
        clients[site] = client

        broadcast(f'{site} joined the Chat')
        # client.send('Connected to the Server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print('Server is Listening ...')
receive()
