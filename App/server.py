from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import json

app = Flask(__name__)
CORS(app)

try:
    ser = serial.Serial('COM3', 115200, timeout=0.1)
except Exception as e:
    print(f"Error: {e}. What Da Helle!")
    ser = None

@app.route('/update', methods=['POST'])
def update():
    if ser and ser.is_open:
        data = request.json
        ser.write((json.dumps(data) + '\n').encode())
        return jsonify({"status": "sent to pico"})
    return jsonify({"status": "offline"}), 400

if __name__ == '__main__':
    app.run(port=5000)