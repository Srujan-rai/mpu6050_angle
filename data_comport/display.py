import tkinter as tk
import serial

# Create a function to update the displayed values
def update_values():
    try:
        # Read data from the COM port (replace 'COM3' with your COM port)
        with serial.Serial('COM6', 9600, timeout=1) as ser:
            data = ser.readline().decode('utf-8').strip()

            # Split the data into roll, yaw, and pitch values (assuming comma-separated values)
            roll, yaw, pitch = map(float, data.split(','))

            # Update the labels with the new values
            roll_label.config(text=f"Roll: {roll:.2f} degrees")
            yaw_label.config(text=f"Yaw: {yaw:.2f} degrees")
            pitch_label.config(text=f"Pitch: {pitch:.2f} degrees")

    except serial.SerialException as e:
        print(f"Error: {e}")

# Create the main window
root = tk.Tk()
root.title("Roll, Yaw, and Pitch Display")

# Create labels to display the values
roll_label = tk.Label(root, text="Roll: 0.00 degrees")
yaw_label = tk.Label(root, text="Yaw: 0.00 degrees")
pitch_label = tk.Label(root, text="Pitch: 0.00 degrees")

# Pack the labels into the window
roll_label.pack()
yaw_label.pack()
pitch_label.pack()

# Create a button to update the values
update_button = tk.Button(root, text="Update Values", command=update_values)
update_button.pack()

# Start the main event loop
root.mainloop()
