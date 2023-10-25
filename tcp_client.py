# Author: Vitor Micilloi
# Author email: vitormicillo@gmail.com

import socket
import argparse
import threading
import sys

# Function to receive messages from server
def receive_messages(client_socket, client_name):
    while True:
        try:
            # Receive and display message
            '''''
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            '''
            message = client_socket.recv(1024).decode('utf-8')
            sys.stdout.write("\r" + " " * (len(client_name) + 2) + "\r")  # clear the previous line
            print(message)
            sys.stdout.write(f"{client_name}: ")
            sys.stdout.flush()


        except:
            # Close the socket upon failure
            client_socket.close()
            break

def run(client_socket, client_name):
    client_socket.send(client_name.encode('utf-8'))
    
    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_name))
    receive_thread.start()

    sys.stdout.write(f"{client_name}: ")
    sys.stdout.flush()

    while True:
        # Send messages to the server
        message = input()
        client_socket.send(message.encode('utf-8'))

        sys.stdout.write(f"{client_name}: ")
        sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301
    

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_addr, server_port))

    run(client_socket, client_name)
