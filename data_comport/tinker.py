import serial
import tkinter as tk

com_port = 'COM4'
baud_rate = 9600

def extract_pitch_roll(data):
    pitch = None
    roll = None
    parts = data.split()
    for part in parts:
        if part.startswith("Pitch:"):
            pitch = float(part.split(":")[1])
        elif part.startswith("Roll:"):
            roll = float(part.split(":")[1])
    return pitch, roll

def update_values():
    data = ser.readline().decode('utf-8').strip()
    if data:
        pitch, roll = extract_pitch_roll(data)
        if pitch is not None:
            pitch_label.config(text=f"Pitch: {pitch}")
        if roll is not None:
            roll_label.config(text=f"Roll: {roll}")
    root.after(100, update_values)

try:
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Reading data from {com_port} at {baud_rate} baud rate...")

    root = tk.Tk()
    root.title("Pitch and Roll Display")

    pitch_label = tk.Label(root, text="Pitch: ")
    pitch_label.pack()

    roll_label = tk.Label(root, text="Roll: ")
    roll_label.pack()

    update_values()

    root.mainloop()

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"{com_port} closed.")
