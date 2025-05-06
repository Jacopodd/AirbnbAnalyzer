import json
from pymongo import MongoClient

# Connessione a MongoDB locale
client = MongoClient("mongodb://localhost:27017")
db = client["airbnbMilano"]

# Mappa dei file e relative collezioni
files_collections = {
    "../data/reviews_cleaned_lines.json": "recensioni",
    "../data/neighbourhoods_cleaned_lines.json": "quartieri"
}

def import_json(file_path, collection_name):
    collection = db[collection_name]
    with open(file_path, "r", encoding="utf-8") as f:
        docs = []
        for line in f:
            try:
                doc = json.loads(line)
                docs.append(doc)
            except json.JSONDecodeError:
                print(f"Errore nel file {file_path}: riga non valida")
        if docs:
            collection.insert_many(docs)
            print(f"Inseriti {len(docs)} documenti in '{collection_name}'")
        else:
            print(f"Nessun documento valido trovato in '{file_path}'")

# Esegui l'import per ogni file
for file, col in files_collections.items():
    import_json(file, col)

print("✅ Importazione completata.")
