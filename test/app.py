import serial
import json
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Set up the serial port (adjust to match your system)
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600)
except serial.SerialException as e:
    ser = None
    print(f"Error opening serial port: {e}")

# Store sensor values
sensor_values = []

# Serve the main page
@app.route('/')
def home():
    return render_template('gas.html')

# Serve the sensor data
@app.route('/sensor-data')
def get_sensor_data():
    if ser and ser.in_waiting > 0:
        sensor_value = ser.readline().decode('utf-8').strip()  # Read data from Arduino
        sensor_values.append(float(sensor_value))  # Store sensor value
        return jsonify({'sensor_value': sensor_value, 'sensor_values': sensor_values})
    else:
        return jsonify({'error': 'No data available'}), 503

if __name__ == '__main__':
    app.run(debug=True)
