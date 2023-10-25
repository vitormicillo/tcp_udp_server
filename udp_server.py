# Author: Vitor Micilloi
# Author email: vitormicillo@gmail.com

import socket

# Global Variables
clients = {}  # To keep track of clients and their addresses

def run(serverSocket, serverPort):
    serverSocket.bind(('127.0.0.1', serverPort))
    print(f"Server running on port {serverPort}")

    while True:
        message, clientAddr = serverSocket.recvfrom(1024)
        message = message.decode('utf-8')

        if clientAddr not in clients:
            # First message is username
            clients[clientAddr] = message
            print(f"Accepted connection from {clientAddr}. Username: {message}")
            continue

        print(f"Message received from ({clientAddr}): {clients[clientAddr]}: {message}")

        # Broadcast the message to all other clients
        for addr in clients:
            if addr != clientAddr:
                serverSocket.sendto(f"{clients[clientAddr]}: {message}".encode('utf-8'), addr)

if __name__ == "__main__":
    serverPort = 9301
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run(serverSocket, serverPort)
