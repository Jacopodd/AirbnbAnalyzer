from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["airbnbMilano"]

alloggi = db["alloggi"]
host = db["host"]

# Cancella eventuali host preesistenti
host.delete_many({})

# Estrai tutti gli host unici da alloggi
hosts_unici = alloggi.aggregate([
    {
        "$group": {
            "_id": "$host_id",  # Raggruppa per host_id
            "nome": { "$first": "$host_nome" }
        }
    }
])

# Inserisci gli host nella collezione host
host_docs = []
for h in hosts_unici:
    host_docs.append({
        "_id": h["_id"],
        "nome": h["nome"]
    })

if host_docs:
    host.insert_many(host_docs)
    print(f"✅ Inseriti {len(host_docs)} host nella collezione 'host'")
else:
    print("⚠️ Nessun host trovato.")
