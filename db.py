from pymongo import MongoClient
import os

def get_db_connection():
    """
    Crea e restituisce la connessione al database MongoDB.
    Il database si chiama 'airbnb_milano'.
    """
    # Puoi cambiare la stringa di connessione se usi MongoDB Atlas o Docker
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["airbnbMilano"]
    return db
