import serial
import tkinter as tk

# Replace 'COM6' with the name of your COM port
com_port = 'COM6'
baud_rate = 9600  # Match this with your Arduino's serial baud rate

def update_values():
    try:
        data = ser.readline().decode('utf-8').strip()
        if data:
            values = data.split(',')
            if len(values) == 3:
                roll_var.set(f"Roll: {values[0]} degrees")
                pitch_var.set(f"Pitch: {values[1]} degrees")
                yaw_var.set(f"Yaw: {values[2]} degrees")

        root.after(100, update_values)  # Update values every 100ms

    except serial.SerialException as e:
        print(f"Error: {e}")

root = tk.Tk()
root.title("Roll, Pitch, and Yaw Display")

roll_var = tk.StringVar()
pitch_var = tk.StringVar()
yaw_var = tk.StringVar()

roll_label = tk.Label(root, textvariable=roll_var)
pitch_label = tk.Label(root, textvariable=pitch_var)
yaw_label = tk.Label(root, textvariable=yaw_var)

roll_label.pack()
pitch_label.pack()
yaw_label.pack()

try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Reading data from {com_port} at {baud_rate} baud rate...")
    update_values()

    root.mainloop()
except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"{com_port} closed.")
