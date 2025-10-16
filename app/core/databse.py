
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

client = AsyncMongoClient(MONGO_URI)
db = client[DB_NAME]

