import os, datetime
from dotenv import load_dotenv
from distutils.util import strtobool
from getmac import get_mac_address

load_dotenv()

# The ID of our sensor. Should be the serial number of the AS1 # 007 = PlutoSDR
SENSOR_ID = '1796F007' + get_mac_address().replace(':', '').upper()

# The period between heartbeats, and between geopositions, in seconds
HEARTBEAT_FREQUENCY_SECONDS = int(os.getenv("HEARTBEAT_FREQUENCY_SECONDS"))

# The URL of the /detection endpoint of the Aerotracker instance we're reporting to
AEROTRACKER_DETECTION_ENDPOINT = os.getenv("AEROTRACKER_DETECTION_ENDPOINT")
AEROTRACKER_HEARTBEAT_ENDPOINT = os.getenv("AEROTRACKER_HEARTBEAT_ENDPOINT")

# The URL of the /detection, /geoposition and /heartbeat endpoints of the Mr.Fusion instance we're reporting to
MR_FUSION_DETECTION_ENDPOINT = os.getenv("MR_FUSION_DETECTION_ENDPOINT")
MR_FUSION_HEARTBEAT_ENDPOINT = os.getenv("MR_FUSION_HEARTBEAT_ENDPOINT")
MR_FUSION_GEOPOSITION_ENDPOINT = os.getenv("MR_FUSION_GEOPOSITION_ENDPOINT")

# The environment the AS1 is currently running in (either dev or prod)
ENV = os.getenv("ENV")

TCP_IP = os.getenv("TCP_IP")
TCP_PORT = int(os.getenv("TCP_PORT"))

# # Log file into which detections data from the Ettus will be saved in CSV format
# DETECTIONS_LOG_FILE = "detections-{0}.csv".format(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
# POSTED_DETECTION_LOG_FILE = "posted-detections-{0}.csv".format(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))

# # Log file into which detections data from the DRI receiver will be saved in CSV format
# DRI_LOG_FILE = "DRI-{0}.csv".format(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
# WIFI_LOG_FILE =  "WIFI-{0}.csv".format(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))   

# DEFAULT_LAT = os.getenv("DEFAULT_LAT")
# DEFAULT_LON = os.getenv("DEFAULT_LON")
# DEFAULT_ALT = os.getenv("DEFAULT_ALT")

# #GPS_POST = strtobool(os.getenv("GPS_POST"))

# PATH_TO_UAV_PROGRAM = os.getenv("PATH_TO_PLUTO_SDR_UAV")
# UAV_PROGRAM_NAME = os.getenv("PATH_TO_PLUTO_SDR_UAV")
# PATH_TO_PLUTO_SDR_START_BUTTON_PNG = os.getenv("PATH_TO_PLUTO_SDR_START_BUTTON_PNG")
# PATH_TO_UAV_PROGRAM_SCANNING_PICTURE = os.getenv("PATH_TO_UAV_PROGRAM_SCANNING_PICTURE")
# PLUTO_SDR_UAV_PROGRAM_NAME = os.getenv("PLUTO_SDR_UAV_PROGRAM_NAME")
# PATH_TO_TCP_LISTENER_PROGRAM = os.getenv("PATH_TO_TCP_LISTENER_PROGRAM")
# TCP_LISTENER_PROGRAM_NAME = os.getenv("TCP_LISTENER_PROGRAM_NAME")