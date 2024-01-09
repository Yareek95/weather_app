from pymongo import MongoClient
import os
from dotenv import load_dotenv
from getpass import getpass

load_dotenv()  # Load environment variables from .env file

# Retrieve the MongoDB password from the environment variable
MONGO_DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD")

# If the password is not set in the environment variable, prompt the user to enter it securely
if not MONGO_DB_PASSWORD:
    MONGO_DB_PASSWORD = getpass("Enter your MongoDB password: ")

try:
    client = MongoClient(f"mongodb+srv://Yarik:{MONGO_DB_PASSWORD}@login.wrtuhbw.mongodb.net/")

    # Check if the connection is successful
    if client.server_info():
        print("Connected to MongoDB Atlas")

        # Specify the database and collection
        db = client["weather-app"]
        collection = db["global_chat"]

        # Define the criteria for documents to delete

        criteria = {"message": "asd"}


        # Delete multiple documents that match the criteria
        result = collection.delete_many(criteria)

        # Print the number of deleted documents
        print(f"Deleted {result.deleted_count} documents")
    else:
        print("Unable to connect to MongoDB Atlas")

except Exception as e:
    print(f"Error: {e}")
