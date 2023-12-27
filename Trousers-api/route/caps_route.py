# trousers_route.py
from flask import Flask, jsonify, request
from model.trousers_model import TrousersModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
print(f"MONGO_URI: {MONGO_URI}")

client = MongoClient(MONGO_URI)
db = client["trousers"]  # Use a different database for trousers

# Check if MongoDB is connected
try:
    client.server_info()
    print("MongoDB connected")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

trousers_collection = db['trousers']

def seed_data():
    # Check if the collection is empty
    if trousers_collection.count_documents({}) == 0:
        trousers_data = [
            TrousersModel(1, 'Casual Trousers', 50.0),
            TrousersModel(2, 'Formal Trousers', 60.0),
            TrousersModel(3, 'Sports Trousers', 45.0)
        ]

        # Insert data into MongoDB
        trousers_collection.insert_many([trousers.to_dict() for trousers in trousers_data])

# Seed data
seed_data()

# Route to get all trousers from MongoDB
@app.route('/trousers', methods=['GET'])
def get_all_trousers():
    trousers_data = list(trousers_collection.find())
    trousers_data_serializable = [{'trousers_id': trousers['trousers_id'], 'trousers_name': trousers['trousers_name'], 'trousers_price': trousers['trousers_price'], '_id': str(trousers['_id'])} for trousers in trousers_data]
    return jsonify({'trousers': trousers_data_serializable})

# Route to get a specific trousers by ID from MongoDB
@app.route('/trousers/<int:trousers_id>', methods=['GET'])
def get_trousers_by_id(trousers_id):
    trousers = trousers_collection.find_one({'trousers_id': trousers_id})
    if trousers:
        trousers_serializable = {'trousers_id': trousers['trousers_id'], 'trousers_name': trousers['trousers_name'], 'trousers_price': trousers['trousers_price'], '_id': str(trousers['_id'])}
        return jsonify({'trousers': trousers_serializable})
    else:
        return jsonify({'message': 'Trousers not found'}), 404

# Route to add new trousers to MongoDB
@app.route('/trousers', methods=['POST'])
def add_trousers():
    data = request.get_json()

    new_trousers = TrousersModel(data['trousers_id'], data['trousers_name'], data['trousers_price'])
    trousers_collection.insert_one(new_trousers.to_dict())

    return jsonify({'message': 'Trousers added successfully'})

# Route to update trousers in MongoDB
@app.route('/trousers/<int:trousers_id>', methods=['PUT'])
def update_trousers(trousers_id):
    data = request.get_json()

    result = trousers_collection.update_one({'trousers_id': trousers_id}, {'$set': {'trousers_name': data['trousers_name'], 'trousers_price': data['trousers_price']}})

    if result.modified_count > 0:
        return jsonify({'message': 'Trousers updated successfully'})
    else:
        return jsonify({'message': 'Trousers not found'}), 404

# Route to delete trousers from MongoDB
@app.route('/trousers/<int:trousers_id>', methods=['DELETE'])
def delete_trousers(trousers_id):
    result = trousers_collection.delete_one({'trousers_id': trousers_id})

    if result.deleted_count > 0:
        return jsonify({'message': 'Trousers deleted successfully'})
    else:
        return jsonify({'message': 'Trousers not found'}), 404

if __name__ == '__main__':
    app.run(port=5004, debug=True)
