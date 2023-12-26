from flask import Flask, jsonify, request
from model.caps_model import CapsModel

app = Flask(__name__)

caps_list = []

def seed_data():
    caps_data = [
        CapsModel(1, 'Classic Cap', 20.0),
        CapsModel(2, 'Sports Cap', 25.0),
        CapsModel(3, 'Fashion Cap', 30.0)
    ]

    caps_list.extend(caps_data)

# Seed data if the list is empty
if not caps_list:
    seed_data()

@app.route('/caps', methods=['GET'])
def get_all_caps():
    return jsonify([cap.to_dict() for cap in caps_list])

@app.route('/caps/<int:cap_id>', methods=['GET'])
def get_cap_by_id(cap_id):
    cap = next((cap for cap in caps_list if cap.cap_id == cap_id), None)
    if cap:
        return jsonify(cap.to_dict())
    else:
        return jsonify({'message': 'Cap not found'}), 404

@app.route('/caps', methods=['POST'])
def add_cap():
    data = request.get_json()

    new_cap = CapsModel(data['cap_id'], data['cap_name'], data['cap_price'])
    caps_list.append(new_cap)

    return jsonify({'message': 'Cap added successfully'})

@app.route('/caps/<int:cap_id>', methods=['PUT'])
def update_cap(cap_id):
    data = request.get_json()

    cap = next((cap for cap in caps_list if cap.cap_id == cap_id), None)
    if cap:
        cap.cap_name = data['cap_name']
        cap.cap_price = data['cap_price']
        return jsonify({'message': 'Cap updated successfully'})
    else:
        return jsonify({'message': 'Cap not found'}), 404

@app.route('/caps/<int:cap_id>', methods=['DELETE'])
def delete_cap(cap_id):
    global caps_list
    caps_list = [cap for cap in caps_list if cap.cap_id != cap_id]
    return jsonify({'message': 'Cap deleted successfully'})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
