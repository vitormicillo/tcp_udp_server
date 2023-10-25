# Author: Vitor Micilloi
# Author email: vitormicillo@gmail.com

import socket
import threading

# Global Variables
clients = []
client_names = {}

# Function to handle each client
def handle_client(client_socket, address):
    global clients
    global client_names

    # Get the client's name (first message after connection)
    client_name = client_socket.recv(1024).decode('utf-8')
    client_names[client_socket] = client_name
    print(f"Accepted connection from {address}. Username: {client_name}")

    while True:
        try:
            # Receiving messages from the client
            message = client_socket.recv(1024)
            if not message:
                break

            print(f"Message recived from ({address}): {client_names[client_socket]}: {message.decode('utf-8')}")


            # Broadcast the message to all other clients
            for client in clients:
                if client != client_socket:
                    client.send(f"{client_names[client_socket]}: {message.decode('utf-8')}".encode('utf-8'))
                    
        except:
            # Remove the client on any failure
            clients.remove(client_socket)
            del client_names[client_socket]
            break

# Main function to run the server
def run(server_socket, server_port):
    global clients

    print(f"Server running on port {server_port}")

    while True:
        # Accept a new client connection
        client_socket, address = server_socket.accept()
        
        # Add the new client to the list
        clients.append(client_socket)

        

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(3)
    
    run(server_socket, server_port)

