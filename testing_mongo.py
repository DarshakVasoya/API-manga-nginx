from pymongo import MongoClient
import urllib.parse

# Define MongoDB connection details
raw_username = "darshakmainz"
raw_password = "Darshak1310@"
encoded_username = urllib.parse.quote_plus(raw_username)
encoded_password = urllib.parse.quote_plus(raw_password)
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@manga.tu41ccq.mongodb.net/?retryWrites=true&w=majority"

try:
    # Create a MongoDB client
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    database = client["manga"]
    collection = database["all_manga"]

    # Check connection
    client.server_info()  # Force a call to the server to check if it's reachable
    print("MongoDB connection successful!")
except Exception as e:
    print(f"An error occurred: {e}")
