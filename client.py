import socket
import sys
import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np
from time import sleep

# --- Configuration ---
# Must match the server's HOST and PORT
SERVER_HOST = '192.168.2.159'
SERVER_PORT = 65432

# --- MatPlotLib Setup ---
style.use('fivethirtyeight')
plt.ion()
fig, ax = plt.subplots()
ax.set_xlabel("Seconds")
ax.set_ylabel("Reading")
ax.set_title("ADXL345 Live Feed")
# Creating lists for each reading
x_vals = []
yX_vals = []
yY_vals = []
yZ_vals = []
line1, = ax.plot(x_vals,yX_vals,'b-')
line2, = ax.plot(x_vals,yY_vals,'r-')
line3, = ax.plot(x_vals,yZ_vals,'g-')
# Connecting to host
print(f"--- Client trying to connect to {SERVER_HOST}:{SERVER_PORT} ---")

# Draw graph with given values
def animate(x,y,z,index):
    x_vals.append(index)
    yX_vals.append(x)
    yY_vals.append(y)
    yZ_vals.append(z)
    line1.set_xdata(x_vals)
    line1.set_ydata(yX_vals)
    line2.set_xdata(x_vals)
    line2.set_ydata(yY_vals)
    line3.set_xdata(x_vals)
    line3.set_ydata(yZ_vals)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()
    sleep(0.5)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # --- Connect to Server ---
        # Initiate connection to the server address and port
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected successfully to the server.")
        # --- Receive Response ---
        # Wait to receive data back from the server (up to 1024 bytes)
        index = 0
        while True:
            data_received = client_socket.recv(1024)
            data = pickle.loads(data_received)
            animate(data[0],data[1],data[2],index)
            index+=1
except socket.error as e:
    print(f"Socket error during connection or communication: {e}")
    print("Is the server running and reachable?")
except ConnectionRefusedError:
     print(f"Connection refused. Make sure the server is running on {SERVER_HOST}:{SERVER_PORT}.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    print("--- Client closing connection ---") # Socket closes automatically due to 'with'