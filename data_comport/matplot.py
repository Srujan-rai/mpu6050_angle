import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import re

com_port = 'COM4'
baud_rate = 9600

pitch_data = []
yaw_data = []

fig, ax = plt.subplots(2, 1)

def extract_pitch_yaw(data):
    # Use regular expressions to find the pitch and yaw values in the string
    pitch_match = re.search(r'Pitch: (-?\d+\.\d+)', data)
    yaw_match = re.search(r'Yaw: (-?\d+\.\d+)', data)

    if pitch_match and yaw_match:
        pitch = float(pitch_match.group(1))
        yaw = float(yaw_match.group(1))
        return pitch, yaw
    else:
        return None, None

def update_plot(frame):
    data = ser.readline().decode('utf-8').strip()

    if data:
        pitch, yaw = extract_pitch_yaw(data)

        if pitch is not None and yaw is not None:
            pitch_data.append(pitch)
            yaw_data.append(yaw)

            ax[0].clear()
            ax[0].plot(pitch_data)
            ax[0].set_title('Pitch Data')

            ax[1].clear()
            ax[1].plot(yaw_data)
            ax[1].set_title('Yaw Data')

try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Reading data from {com_port} at {baud_rate} baud rate...")

    ani = FuncAnimation(fig, update_plot, interval=100)  # Update every 100 milliseconds

    plt.show()

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"{com_port} closed.")
