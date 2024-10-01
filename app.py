from http.client import InvalidURL
from bson import ObjectId
from flask import Flask, jsonify
from pymongo import MongoClient
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

# Get Manga entries with dynamic page number (excluding chapters)
@app.route("/manga/page/<int:page_number>", methods=["GET"])
def list_manga(page_number):
    limit = 20  # Number of manga entries per page
    skip = page_number * limit

    mangas = collection.find({}, {'chapters': 0})  # Exclude chapters
    mangas = mangas.skip(skip).limit(limit)

    return jsonify([mongo_item_to_json(manga) for manga in mangas])

# Get a list of all manga titles for searching
@app.route("/manga_list", methods=["GET"])
def all_manga_titles():
    mangas = collection.find({}, {'title': 1})
    return jsonify([mongo_item_to_json(manga) for manga in mangas])

# Get Manga entry by ID
@app.route("/manga/id/<string:manga_id>", methods=["GET"])
def get_manga_by_id(manga_id):
    try:
        manga = collection.find_one({'_id': ObjectId(manga_id)}, {'chapters': 0})  # Exclude chapters
        if manga:
            return jsonify(mongo_item_to_json(manga))
        else:
            return jsonify({"error": "Manga not found"}), 404
    except InvalidURL:
        return jsonify({"error": "Invalid ID format"}), 400

# Get Manga entry by slug
@app.route("/manga/<string:manga_slug>", methods=["GET"])
def get_manga_by_slug(manga_slug):
    manga_slug = manga_slug.replace("-", " ").title().replace("’S", "’s").replace("’t", "’t")
    print(manga_slug)
    manga = collection.find_one({'title': manga_slug}, {'chapters': 0})  # Exclude chapters
    if manga:
        return jsonify(mongo_item_to_json(manga))
    else:
        return jsonify({"error": "Manga not found"}), 404

    
# Get a specific chapter of a particular manga
@app.route("/manga/<string:manga_slug>/chapter/<int:chapter_number>", methods=["GET"])
def get_manga_chapter(manga_slug, chapter_number):
    # Find the manga by slug

    manga_slug = manga_slug.replace("-", " ").title().replace("’S", "’s").replace("’t", "’t")
 
    manga = collection.find_one({'title': manga_slug})  
    
    if manga is None:
        return jsonify({"error": "Manga not found"}), 404

    # Check if the chapter exists
    chapter_key = f"Chapter {chapter_number}"

    chapter_images = manga["chapters"].get(chapter_key)
 
    if chapter_images is None:
        return jsonify({"error": "Chapter not found"}), 404
       

    # Return the chapter images
    return jsonify({
        "title": manga["title"],
        "chapter": chapter_key,
        "images": chapter_images
    })

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
