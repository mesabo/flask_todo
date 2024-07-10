import os
import motor.motor_asyncio
from dotenv import load_dotenv
from flask import current_app

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
hostname = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database_name = os.getenv("DB_NAME")
baseurl = os.getenv("MONGO_BASE_URL")
baseurlrules = os.getenv("MONGO_URL_RULES")

mongo_uri = f"{baseurl}{username}:{password}@{hostname}:{port}{baseurlrules}"

class DataBase:
    client: motor.motor_asyncio.AsyncIOMotorClient = None

db = DataBase()

def init_db(app):
    @app.before_request
    def before_request():
        # Ensure MongoDB client is initialized
        if db.client is None:
            db.client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
            current_app.logger.info("Connected to MongoDB")

def get_database() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return db.client[database_name]
