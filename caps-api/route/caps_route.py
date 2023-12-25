# caps/route/caps_route.py
from flask import Flask, jsonify
from model.caps_model import Caps

app = Flask(__name__)

# Sample data for demonstration
caps_data = [
    Caps(1, 'Classic Cap', 20.0),
    Caps(2, 'Sports Cap', 25.0),
    Caps(3, 'Fashion Cap', 30.0)
]

@app.route('/caps', methods=['GET'])
def get_all_caps():
    caps_list = [cap.to_dict() for cap in caps_data]
    return jsonify(caps_list)

@app.route('/caps/<int:cap_id>', methods=['GET'])
def get_cap_by_id(cap_id):
    cap = next((cap for cap in caps_data if cap.cap_id == cap_id), None)
    if cap:
        return jsonify(cap.to_dict())
    else:
        return jsonify({'message': 'Cap not found'}), 404
