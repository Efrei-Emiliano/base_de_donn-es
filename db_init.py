from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["char"]
def get_characters():
    return list(db.character.find())
def get_scores():
    return list(db.scores.find())
def get_enemy():
    return list(db.enemy.find())