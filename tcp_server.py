import socket
import threading
import json, requests, os, time

from json import JSONDecoder
from consts import *

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

            # print(f"Message recived from ({address}): {client_names[client_socket]}: {message.decode('utf-8')}")
            print(f"{message.decode('utf-8')}")
            
            print(f"sensor-id from auto detection {SENSOR_ID}")

            # if AEROTRACKER_DETECTION_ENDPOINT != "":
            #         print("[plutosdr_detection] - Sending detection to AeroTracker...")
            #         postDetections(message.decode('utf-8'), AEROTRACKER_DETECTION_ENDPOINT, "1796F007000a35000122")

            if MR_FUSION_DETECTION_ENDPOINT != "":
                    postDetections(message.decode('utf-8'), MR_FUSION_DETECTION_ENDPOINT, "1796F007000A35000122")
                    postHeartBeat(MR_FUSION_HEARTBEAT_ENDPOINT, "1796F007000A35000122")
                    postSensorGeoposition(MR_FUSION_GEOPOSITION_ENDPOINT, "1796F007000A35000122")

            # Broadcast the message to all other clients
            for client in clients:
                if client != client_socket:
                    client.send(f"{client_names[client_socket]}: {message.decode('utf-8')}".encode('utf-8'))
                    
        except:
            # Remove the client on any failure
            clients.remove(client_socket)
            del client_names[client_socket]
            break

def postSensorGeoposition(geoposition_endpoint, sensor_id):
    try:
        gp = requests.post(
            geoposition_endpoint,
            json={
                "sensor-id": f"{sensor_id}",
                "time": int(time.time() * 1000), # Convert seconds to milliseconds
                "position": {
                    "latitude": 53.314829,
                    "longitude": -0.951597,
                    "accuracy": 1.0
                }
            },
            timeout=3.0
        )
        print(f"{gp.text}")

    except Exception as e:
        print(f"Geoposition error: {e}")

def postHeartBeat(heartbeat_endpoint, sensor_id):
    try:
        hb = requests.post(
            heartbeat_endpoint,
            json={
                "sensor-id": f"{sensor_id}",
                "time": int(time.time() * 1000) # Convert seconds to milliseconds
            },
            timeout=3.0
        )
        print(f"{hb.text}")

    except Exception as e:
        print(f"Heartbeat error: {e}")

def postDetections(drone_detection, endpoint, sensor_id):      
    print(drone_detection)
    
    try:
        r = requests.post(
            endpoint,
            json={
                "sensor-id": sensor_id,
                "time": int(time.time() * 1000), # Convert seconds to milliseconds
                "position": {
                    "latitude": float(drone_detection.get('deviceLat',0)),
                    "longitude": float(drone_detection.get('deviceLng',0)),
                    "altitude": float(drone_detection.get('altitude', 0)), #In DRI, the barometric altitude is "height".
                    "accuracy": 1.0, # +/- meters
                    "speed-horizontal": float(drone_detection.get('drone',{}).get('speed',0)),
                    "bearing": float(drone_detection.get('drone',{}).get('bearing',0)) % 360
                },
                "metadata": [
                    {
                        "key": "type",
                        "val": "drone"
                    },{
                        "key": "mac_address",
                        "val": str(drone_detection.get('drone',{}).get('mac_address',"PLACEHOLDER_MAC_ADDRESS")),
                        "type": "primary"
                    },{
                        "key": "source",
                        "val": str(drone_detection.get('drone',{}).get('mac_address',"PLACEHOLDER_MAC_ADDRESS")),
                        "type": "primary"
                    },{
                        "key": "runtime",
                        "val": str(drone_detection.get('sensor',{}).get('runtime',0)),
                        "type": "primary"
                    },{
                        "key": "registration",
                        "val": str(drone_detection.get('deviceId', "PLACEHOLDER_DRONE_ID")),
                        "type": "primary"
                    },{
                        "key": "icao",
                        "val": str(drone_detection.get('drone',{}).get('drone_id',"PLACEHOLDER_DRONE_ID")),
                        "type": "primary"
                    },{
                        "key": "alt",
                        "val": str(drone_detection.get('drone',{}).get('altitude',0)),
                        "type": "volatile"
                    }
                ]
            },
            timeout=1.0
        )

        print(f"[postDetection] - response from {endpoint}: {r.text}")
    except Exception as e:
        print(f"{e}")

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
    server_port = TCP_PORT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, server_port))
    server_socket.listen(3)
    
    run(server_socket, server_port)

