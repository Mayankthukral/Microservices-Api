from flask import Flask, jsonify, request
from model.shirts_model import ShirtsModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI_SHIRTS")  # Update the environment variable name
print(f"MONGO_URI: {MONGO_URI}")

client = MongoClient(MONGO_URI)
db = client["shirts"]  # Update the database name

# Check if MongoDB is connected
try:
    client.server_info()
    print("MongoDB connected")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

shirts_collection = db['shirts']

def seed_data():
    # Check if the collection is empty
    if shirts_collection.count_documents({}) == 0:
        shirts_data = [
            ShirtsModel(1, 'Casual Shirt', 40.0),
            ShirtsModel(2, 'Formal Shirt', 50.0),
            ShirtsModel(3, 'Denim Shirt', 45.0)
        ]

        # Insert data into MongoDB
        shirts_collection.insert_many([shirt.to_dict() for shirt in shirts_data])

# Seed data
seed_data()

# Route to get all shirts from MongoDB
@app.route('/shirts', methods=['GET'])
def get_all_shirts():
    shirts_data = list(shirts_collection.find())
    shirts_data_serializable = [{'shirt_id': shirt['shirt_id'], 'shirt_name': shirt['shirt_name'], 'shirt_price': shirt['shirt_price'], '_id': str(shirt['_id'])} for shirt in shirts_data]
    return jsonify({'shirts': shirts_data_serializable})

# Route to get a specific shirt by ID from MongoDB
@app.route('/shirts/<int:shirt_id>', methods=['GET'])
def get_shirt_by_id(shirt_id):
    shirt = shirts_collection.find_one({'shirt_id': shirt_id})
    if shirt:
        shirt_serializable = {'shirt_id': shirt['shirt_id'], 'shirt_name': shirt['shirt_name'], 'shirt_price': shirt['shirt_price'], '_id': str(shirt['_id'])}
        return jsonify({'shirt': shirt_serializable})
    else:
        return jsonify({'message': 'Shirt not found'}), 404

# Route to add a new shirt to MongoDB
@app.route('/shirts', methods=['POST'])
def add_shirt():
    data = request.get_json()

    new_shirt = ShirtsModel(data['shirt_id'], data['shirt_name'], data['shirt_price'])
    shirts_collection.insert_one(new_shirt.to_dict())

    return jsonify({'message': 'Shirt added successfully'})

# Route to update a shirt in MongoDB
@app.route('/shirts/<int:shirt_id>', methods=['PUT'])
def update_shirt(shirt_id):
    data = request.get_json()

    result = shirts_collection.update_one({'shirt_id': shirt_id}, {'$set': {'shirt_name': data['shirt_name'], 'shirt_price': data['shirt_price']}})

    if result.modified_count > 0:
        return jsonify({'message': 'Shirt updated successfully'})
    else:
        return jsonify({'message': 'Shirt not found'}), 404

# Route to delete a shirt from MongoDB
@app.route('/shirts/<int:shirt_id>', methods=['DELETE'])
def delete_shirt(shirt_id):
    result = shirts_collection.delete_one({'shirt_id': shirt_id})

    if result.deleted_count > 0:
        return jsonify({'message': 'Shirt deleted successfully'})
    else:
        return jsonify({'message': 'Shirt not found'}), 404

if __name__ == '__main__':
    app.run(port=5003, debug=True)  # Update the port number
