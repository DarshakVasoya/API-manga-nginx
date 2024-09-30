from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import urllib.parse
from flask_cors import CORS 


# Define MongoDB connection details
raw_username = "darshakmainz"
raw_password = "Darshak1310@"
encoded_username = urllib.parse.quote_plus(raw_username)
encoded_password = urllib.parse.quote_plus(raw_password)
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@manga.tu41ccq.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoDB client
client = MongoClient(uri)
database = client["manga"]
collection = database["all_manga"]

# Create Flask app
app = Flask(__name__)
CORS(app)

# Helper function to convert MongoDB documents to JSON-serializable format
def mongo_item_to_json(item):
    item["_id"] = str(item["_id"])
    return item



# Get all Manga entries
@app.route("/", methods=["GET"])
def list_manga():
    mangas = collection.find().limit(10)
    return jsonify([mongo_item_to_json(manga) for manga in mangas])



# Run the Flask app
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host='0.0.0.0',debug=True)
