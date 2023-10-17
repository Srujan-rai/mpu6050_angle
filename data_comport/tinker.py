import serial
import tkinter as tk

com_port = 'COM4'
baud_rate = 9600


# Create a function to update the GUI with new data
def update_gui():
    data = ser.readline().decode('utf-8').strip()
    if data:
        components = data.split(', ')
        pitch, roll, yaw = None, None, None
        for component in components:
            if component.startswith("pitch:"):
                pitch = float(component.split(': ')[1])
            elif component.startswith("roll:"):
                roll = float(component.split(': ')[1])
            elif component.startswith("yaw:"):
                yaw = float(component.split(': ')[1])

        if pitch is not None and roll is not None and yaw is not None:
            pitch_label.config(text=f"Pitch: {pitch}")
            roll_label.config(text=f"Roll: {roll}")
            yaw_label.config(text=f"Yaw: {yaw}")

    root.after(100, update_gui)  # Schedule the function to run periodically


try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Reading data from {com_port} at {baud_rate} baud rate...")

    root = tk.Tk()
    root.title("Pitch, Roll, and Yaw Data")

    pitch_label = tk.Label(root, text="Pitch: N/A")
    roll_label = tk.Label(root, text="Roll: N/A")
    yaw_label = tk.Label(root, text="Yaw: N/A")

    pitch_label.pack()
    roll_label.pack()
    yaw_label.pack()

    update_gui()  # Start updating the GUI

    root.mainloop()

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"{com_port} closed.")
print(data)  # Add this line for debugging
