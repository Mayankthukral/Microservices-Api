from flask import Flask, jsonify, request
from model.jeans_model import JeansModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
print(f"MONGO_URI: {MONGO_URI}")

client = MongoClient(MONGO_URI)
db = client["jeans"]

# Check if MongoDB is connected
try:
    client.server_info()
    print("MongoDB connected")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

jeans_collection = db['jeans']

def seed_data():
    # Check if the collection is empty
    if jeans_collection.count_documents({}) == 0:
        jeans_data = [
            JeansModel(1, 'Blue Jeans', 'Slim Fit', 50.0),
            JeansModel(2, 'Black Jeans', 'Regular Fit', 45.0),
            JeansModel(3, 'Distressed Jeans', 'Skinny Fit', 55.0)
        ]

        # Insert data into MongoDB
        jeans_collection.insert_many([jeans.to_dict() for jeans in jeans_data])

# Seed data
seed_data()

# Route to get all jeans from MongoDB
@app.route('/jeans', methods=['GET'])
def get_all_jeans():
    jeans_data = list(jeans_collection.find())
    jeans_data_serializable = [{'jeans_id': jeans['jeans_id'], 'jeans_name': jeans['jeans_name'], 'jeans_fit': jeans['jeans_fit'], 'jeans_price': jeans['jeans_price'], '_id': str(jeans['_id'])} for jeans in jeans_data]
    return jsonify({'jeans': jeans_data_serializable})

# Route to get a specific jeans by ID from MongoDB
@app.route('/jeans/<int:jeans_id>', methods=['GET'])
def get_jeans_by_id(jeans_id):
    jeans = jeans_collection.find_one({'jeans_id': jeans_id})
    if jeans:
        jeans_serializable = {'jeans_id': jeans['jeans_id'], 'jeans_name': jeans['jeans_name'], 'jeans_fit': jeans['jeans_fit'], 'jeans_price': jeans['jeans_price'], '_id': str(jeans['_id'])}
        return jsonify({'jeans': jeans_serializable})
    else:
        return jsonify({'message': 'Jeans not found'}), 404

# Route to add a new jeans to MongoDB
@app.route('/jeans', methods=['POST'])
def add_jeans():
    data = request.get_json()

    new_jeans = JeansModel(data['jeans_id'], data['jeans_name'], data['jeans_fit'], data['jeans_price'])
    jeans_collection.insert_one(new_jeans.to_dict())

    return jsonify({'message': 'Jeans added successfully'})

# Route to update jeans in MongoDB
@app.route('/jeans/<int:jeans_id>', methods=['PUT'])
def update_jeans(jeans_id):
    data = request.get_json()

    result = jeans_collection.update_one({'jeans_id': jeans_id}, {'$set': {'jeans_name': data['jeans_name'], 'jeans_fit': data['jeans_fit'], 'jeans_price': data['jeans_price']}})

    if result.modified_count > 0:
        return jsonify({'message': 'Jeans updated successfully'})
    else:
        return jsonify({'message': 'Jeans not found'}), 404

# Route to delete jeans from MongoDB
@app.route('/jeans/<int:jeans_id>', methods=['DELETE'])
def delete_jeans(jeans_id):
    result = jeans_collection.delete_one({'jeans_id': jeans_id})

    if result.deleted_count > 0:
        return jsonify({'message': 'Jeans deleted successfully'})
    else:
        return jsonify({'message': 'Jeans not found'}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)
