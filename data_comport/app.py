import serial
from flask import Flask, request, render_template


app = Flask(__name__)

com_port = 'COM4'
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate, timeout=1)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = ser.readline().decode('utf-8').strip()
    if data:
        pitch, roll = extract_pitch_roll(data)
        return f'Pitch: {pitch}, Roll: {roll}'
    return 'No data available'

if __name__ == '__main__':
    app.run(debug=True)
