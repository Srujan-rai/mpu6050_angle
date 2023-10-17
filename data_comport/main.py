import serial

com_port = 'COM4'
baud_rate = 9600

try:

    ser = serial.Serial(com_port, baud_rate, timeout=1)
    print(f"Reading data from {com_port} at {baud_rate} baud rate...")

    while True:

        data = ser.readline().decode('utf-8').strip()


        if data:
            print(data)

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"{com_port} closed.")
