from flask import Flask, render_template, request, jsonify
import serial

app = Flask(__name__)
#ser = serial.Serial('/dev/ttyUSB0', 9600)  

class MockSerial:
    def __init__(self):
        self.data = ""

    def write(self, command):
        self.data = command
        self.process_command(command)

    def process_command(self, command):
        if command.startswith(b"SPEED:"):
            speed = command.decode().split(":")[1].strip()
            print(f"Setting speed to {speed}")
        elif command.startswith(b"DIR:"):
            direction = command.decode().split(":")[1].strip()
            print(f"Setting direction to {direction}")

    def close(self):
        print("Closing mock serial connection")

# Replace the actual serial.Serial with MockSerial in your Flask app
ser = MockSerial()


@app.route('/')
def home():
    return render_template('stepper.html')

@app.route('/set-speed', methods=['POST'])
def set_speed():
    speed = request.json['speed']
    ser.write(f"SPEED:{speed}\n".encode())
    return jsonify(success=True)

@app.route('/set-direction', methods=['POST'])
def set_direction():
    direction = request.json['direction']
    ser.write(f"DIR:{direction}\n".encode())
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
