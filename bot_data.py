from pymongo import MongoClient, errors
import os

# 🗝️ MongoDB URI from environment variable (with fallback)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    # ✅ Connect to MongoDB
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Force connection to test if it's working
    mongo_client.admin.command('ping')
    print("✅ Connected to MongoDB!")
except errors.ServerSelectionTimeoutError as err:
    print(f"❌ MongoDB Connection Error: {err}")
    mongo_client = None

if mongo_client:
    # 📂 Select database
    db = mongo_client["bot_database"]  # Replace with your DB name

    # 📁 Select collections
    users_collection = db["users"]
    groups_collection = db["groups"]

    # ✅ Function to save user
    def save_user(user_id: int):
        try:
            if not users_collection.find_one({"user_id": user_id}):
                users_collection.insert_one({"user_id": user_id})
                print(f"✅ Added user {user_id} to database.")
            else:
                print(f"ℹ️ User {user_id} already exists in database.")
        except Exception as e:
            print(f"❌ Error saving user {user_id}: {e}")

    # ✅ Function to save group
    def save_group(chat_id: int):
        try:
            if not groups_collection.find_one({"chat_id": chat_id}):
                groups_collection.insert_one({"chat_id": chat_id})
                print(f"✅ Added group {chat_id} to database.")
            else:
                print(f"ℹ️ Group {chat_id} already exists in database.")
        except Exception as e:
            print(f"❌ Error saving group {chat_id}: {e}")

    # ✅ Function to get total stats
    def get_total_stats():
        try:
            total_users = users_collection.count_documents({})
            total_groups = groups_collection.count_documents({})
            return total_users, total_groups
        except Exception as e:
            print(f"❌ Error fetching stats: {e}")
            return 0, 0

else:
    # ⚠️ MongoDB not connected, fallback to no-op functions
    def save_user(user_id: int):
        print("⚠️ MongoDB not connected. Skipping save_user.")

    def save_group(chat_id: int):
        print("⚠️ MongoDB not connected. Skipping save_group.")

    def get_total_stats():
        print("⚠️ MongoDB not connected. Returning 0 stats.")
        return 0, 0
