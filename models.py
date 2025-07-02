from pymongo import MongoClient
from datetime import datetime
from config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubEventDB:
    def __init__(self):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client[Config.MONGO_DB_NAME]
            self.collection = self.db[Config.MONGO_COLLECTION_NAME]
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def insert_event(self, event_data):
        """Insert a new GitHub event into the database"""
        try:
            result = self.collection.insert_one(event_data)
            logger.info(f"Inserted event with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Failed to insert event: {e}")
            return None

    def get_recent_events(self, limit=50):
        """Get recent events from the database, sorted by timestamp"""
        try:
            events = list(self.collection.find().sort("timestamp", -1).limit(limit))
            # Convert ObjectId to string for JSON serialization
            for event in events:
                event['_id'] = str(event['_id'])
            return events
        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            return []

    def close_connection(self):
        """Close the database connection"""
        if self.client:
            self.client.close()

class GitHubEvent:
    @staticmethod
    def create_push_event(payload):
        """Create a push event document"""
        return {
            "event_type": "push",
            "author": payload.get("pusher", {}).get("name", "Unknown"),
            "to_branch": payload.get("ref", "").replace("refs/heads/", ""),
            "from_branch": None,
            "repository": payload.get("repository", {}).get("name", ""),
            "timestamp": datetime.utcnow(),
            "commits": len(payload.get("commits", [])),
            "raw_payload": payload
        }

    @staticmethod
    def create_pull_request_event(payload):
        """Create a pull request event document"""
        pr = payload.get("pull_request", {})
        return {
            "event_type": "pull_request",
            "author": pr.get("user", {}).get("login", "Unknown"),
            "to_branch": pr.get("base", {}).get("ref", ""),
            "from_branch": pr.get("head", {}).get("ref", ""),
            "repository": payload.get("repository", {}).get("name", ""),
            "timestamp": datetime.utcnow(),
            "action": payload.get("action", ""),
            "pr_number": pr.get("number", ""),
            "raw_payload": payload
        }

    @staticmethod
    def create_merge_event(payload):
        """Create a merge event document"""
        pr = payload.get("pull_request", {})
        return {
            "event_type": "merge",
            "author": pr.get("merged_by", {}).get("login", "Unknown"),
            "to_branch": pr.get("base", {}).get("ref", ""),
            "from_branch": pr.get("head", {}).get("ref", ""),
            "repository": payload.get("repository", {}).get("name", ""),
            "timestamp": datetime.utcnow(),
            "pr_number": pr.get("number", ""),
            "raw_payload": payload
        } 