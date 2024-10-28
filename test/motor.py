from flask import Flask, render_template, jsonify
from time import sleep

app = Flask(__name__)

# Mock Servo class
class MockServo:
    def __init__(self, pin):
        self.pin = pin
        self.position = 0  # Assume position is in degrees

    def max(self):
        self.position = 95  # Simulate moving to 95 degrees
        print(f"Servo on pin {self.pin} moved to {self.position} degrees.")

    def min(self):
        self.position = 0  # Simulate moving to 0 degrees
        print(f"Servo on pin {self.pin} moved to {self.position} degrees.")

# Define mock GPIO pins for servos
servo_pins = [17, 27, 22, 23, 24]  # Change GPIO pins as necessary
servos = [MockServo(pin) for pin in servo_pins]

@app.route('/') 
def index():
    return render_template('motors.html')

@app.route('/move_servo/<int:servo_index>/<string:action>', methods=['GET'])
def move_servo(servo_index, action):
    if 0 <= servo_index < len(servos):
        if action == 'on':
            servos[servo_index].max()  # Simulate moving to max position (95 degrees)
            sleep(3)  # Wait for 1 second for servo to reach position
            servos[servo_index].min()  # Simulate moving back to min position (0 degrees)
        return jsonify({'status': 'success', 'servo_index': servo_index, 'action': action})
    return jsonify({'status': 'error', 'message': 'Invalid servo index'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
