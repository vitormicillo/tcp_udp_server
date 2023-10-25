import socket
import argparse
import threading
import sys

def receive_messages(clientSocket, clientname):
    while True:
        message, _ = clientSocket.recvfrom(1024)
        message = message.decode('utf-8')
        
        sys.stdout.write("\r" + " " * (len(clientname) + 2) + "\r")  # clear the previous line
        print(message)
        sys.stdout.write(f"{clientname}: ")
        sys.stdout.flush()


     

def run(clientSocket, clientname, serverAddr, serverPort):
    clientSocket.sendto(clientname.encode('utf-8'), (serverAddr, serverPort))
    receive_thread = threading.Thread(target=receive_messages, args=(clientSocket, clientname))
    receive_thread.start()

    while True:
        message = input(f"{clientname}: ")
        clientSocket.sendto(message.encode('utf-8'), (serverAddr, serverPort))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argument parser')
    parser.add_argument('name')
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    run(clientSocket, clientname, serverAddr, serverPort)
