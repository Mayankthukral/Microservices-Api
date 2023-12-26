from flask import Flask, jsonify, request
from model.caps_model import CapsModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
print(f"MONGO_URI: {MONGO_URI}")

client = MongoClient(MONGO_URI)
db = client["caps"]

# Check if MongoDB is connected
try:
    client.server_info()
    print("MongoDB connected")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

caps_collection = db['caps']

def seed_data():
    # Check if the collection is empty
    if caps_collection.count_documents({}) == 0:
        caps_data = [
            CapsModel(1, 'Classic Cap', 20.0),
            CapsModel(2, 'Sports Cap', 25.0),
            CapsModel(3, 'Fashion Cap', 30.0)
        ]

        # Insert data into MongoDB
        caps_collection.insert_many([cap.to_dict() for cap in caps_data])

# Seed data
seed_data()

# Route to get all caps from MongoDB
@app.route('/caps', methods=['GET'])
def get_all_caps():
    caps_data = list(caps_collection.find())
    caps_data_serializable = [{'cap_id': cap['cap_id'], 'cap_name': cap['cap_name'], 'cap_price': cap['cap_price'], '_id': str(cap['_id'])} for cap in caps_data]
    return jsonify({'caps': caps_data_serializable})

# Route to get a specific cap by ID from MongoDB
@app.route('/caps/<int:cap_id>', methods=['GET'])
def get_cap_by_id(cap_id):
    cap = caps_collection.find_one({'cap_id': cap_id})
    if cap:
        cap_serializable = {'cap_id': cap['cap_id'], 'cap_name': cap['cap_name'], 'cap_price': cap['cap_price'], '_id': str(cap['_id'])}
        return jsonify({'cap': cap_serializable})
    else:
        return jsonify({'message': 'Cap not found'}), 404

# Route to add a new cap to MongoDB
@app.route('/caps', methods=['POST'])
def add_cap():
    data = request.get_json()

    new_cap = CapsModel(data['cap_id'], data['cap_name'], data['cap_price'])
    caps_collection.insert_one(new_cap.to_dict())

    return jsonify({'message': 'Cap added successfully'})

# Route to update a cap in MongoDB
@app.route('/caps/<int:cap_id>', methods=['PUT'])
def update_cap(cap_id):
    data = request.get_json()

    result = caps_collection.update_one({'cap_id': cap_id}, {'$set': {'cap_name': data['cap_name'], 'cap_price': data['cap_price']}})

    if result.modified_count > 0:
        return jsonify({'message': 'Cap updated successfully'})
    else:
        return jsonify({'message': 'Cap not found'}), 404

# Route to delete a cap from MongoDB
@app.route('/caps/<int:cap_id>', methods=['DELETE'])
def delete_cap(cap_id):
    result = caps_collection.delete_one({'cap_id': cap_id})

    if result.deleted_count > 0:
        return jsonify({'message': 'Cap deleted successfully'})
    else:
        return jsonify({'message': 'Cap not found'}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
