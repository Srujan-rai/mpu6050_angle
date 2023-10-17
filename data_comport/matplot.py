import serial
import matplotlib.pyplot as plt
from collections import deque

com_port = 'COM4'
baud_rate = 9600
max_data_points = 100  # Number of data points to display
y_lim_pitch = (-180, 180)  # Y-axis limits for pitch
y_lim_roll = (-180, 180)  # Y-axis limits for roll
y_lim_yaw = (-180, 180)  # Y-axis limits for yaw

pitch_data = deque(maxlen=max_data_points)
roll_data = deque(maxlen=max_data_points)
yaw_data = deque(maxlen=max_data_points)

plt.ion()  # Turn on interactive mode for real-time plotting

fig, ax = plt.subplots()
line_pitch, = ax.plot([], label="Pitch")
line_roll, = ax.plot([], label="Roll")
line_yaw, = ax.plot([], label="Yaw")

ax.set_xlabel("Time")
ax.set_ylabel("Values")
ax.set_title("Pitch, Roll, and Yaw Data")
ax.legend()

# Set custom Y-axis limits
ax.set_ylim(y_lim_pitch[0], y_lim_pitch[1])

# Create a function to update the plot
def update_plot():
    data = ser.readline().decode('utf-8').strip()
    if data:
        try:
            values = data.split()  # Split the data into individual values
            pitch = float(values[1])
            roll = float(values[3])
            yaw = float(values[5])
            pitch_data.append(pitch)
            roll_data.append(roll)
            yaw_data.append(yaw)
            line_pitch.set_data(range(len(pitch_data)), pitch_data)
            line_roll.set_data(range(len(roll_data)), roll_data)
            line_yaw.set_data(range(len(yaw_data)), yaw_data)

            # Automatically update Y-axis limits based on the data
            ax.relim()
            ax.autoscale_view()

            # Set custom Y-axis limits
            ax.set_ylim(y_lim_pitch[0], y_lim_pitch[1])

            fig.canvas.flush_events()
        except (ValueError, IndexError):
            print(f"Invalid data format: {data}")

try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Reading data from {com_port} at {baud_rate} baud rate...")

    while True:
        update_plot()

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"{com_port} closed.")
