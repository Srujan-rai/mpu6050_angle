import serial
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Replace 'COM3' with the name of your COM port
com_port = 'COM4'
baud_rate = 9600  # Match this with your Arduino's serial baud rate

# Create lists to store pitch, roll, and yaw data
pitch_data = []
roll_data = []
yaw_data = []

# Create a function to update the 3D plot with new data
def update_3d_plot():
    try:
        data = ser.readline().decode('utf-8').strip()
        print(data)
        if data:
            values = data.split(',')
            if len(values) == 3:
                pitch_data.append(float(values[0]))
                roll_data.append(float(values[1]))
                yaw_data.append(float(values[2]))

                # Limit the number of data points shown on the plot
                max_data_points = 50
                if len(pitch_data) > max_data_points:
                    pitch_data.pop(0)
                    roll_data.pop(0)
                    yaw_data.pop(0)

                # Clear and update the 3D plot
                ax.clear()
                ax.scatter(pitch_data, roll_data, yaw_data, c='b', marker='o')
                ax.set_xlabel('Pitch (degrees)')
                ax.set_ylabel('Roll (degrees)')
                ax.set_zlabel('Yaw (degrees)')
                ax.set_title('Orientation in 3D Space')
                canvas.draw()

    except serial.SerialException as e:
        print(f"Error: {e}")

# Create a serial connection
ser = serial.Serial(com_port, baud_rate, timeout=1)

# Create the GUI window
root = tk.Tk()
root.title("MPU6050 3D Data Visualization")

# Create a frame for the 3D plot
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a Matplotlib 3D figure and axis for the plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Create a 3D scatter plot
ax.scatter([], [], [], c='b', marker='o')
ax.set_xlabel('Pitch (degrees)')
ax.set_ylabel('Roll (degrees)')
ax.set_zlabel('Yaw (degrees)')
ax.set_title('Orientation in 3D Space')

# Create a Matplotlib canvas for the 3D plot
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

# Create a function to periodically update the plot
def update_plot():
    update_3d_plot()
    root.after(1000, update_plot)

# Start updating the plot
update_plot()

# Start the main loop
root.mainloop()

# Close the serial connection when the GUI is closed
if 'ser' in locals() and ser.is_open:
    ser.close()
