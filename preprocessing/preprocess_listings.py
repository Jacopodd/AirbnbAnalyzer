import pandas as pd
import json
from pathlib import Path

# === Percorsi relativi ===
INPUT_CSV = "../data/listings.csv"
OUTPUT_JSON = "../data/listings_cleaned.json"

# === Caricamento ===
df = pd.read_csv(INPUT_CSV, low_memory=False)

# === Selezione + rinomina colonne ===
df = df[[
    "id", "name", "host_id", "host_name",
    "neighbourhood_cleansed", "latitude", "longitude",
    "room_type", "property_type", "price", "minimum_nights", "maximum_nights",
    "accommodates", "bedrooms", "beds", "bathrooms_text", "amenities",
    "availability_365", "number_of_reviews", "last_review", "reviews_per_month",
    "review_scores_rating", "instant_bookable"
]].rename(columns={
    "id": "_id",
    "name": "titolo",
    "host_id": "host_id",
    "host_name": "host_nome",
    "neighbourhood_cleansed": "zona",
    "room_type": "tipo_stanza",
    "property_type": "tipologia_alloggio",
    "price": "prezzo_base",
    "minimum_nights": "min_notti",
    "maximum_nights": "max_notti",
    "accommodates": "posti_letto",
    "bedrooms": "camere",
    "beds": "letti",
    "bathrooms_text": "bagni_descrizione",
    "amenities": "servizi",
    "availability_365": "disponibilita_annuale",
    "number_of_reviews": "recensioni_totali",
    "last_review": "ultima_recensione",
    "reviews_per_month": "recensioni_mensili",
    "review_scores_rating": "rating",
    "instant_bookable": "prenotazione_immediata"
})

# === Conversioni dati ===
df["_id"] = df["_id"].astype(str)
df["host_id"] = df["host_id"].astype(str)

# Converti "t"/"f" in booleani
df["prenotazione_immediata"] = df["prenotazione_immediata"].map({'t': True, 'f': False})

# Rimuove simboli $ e converte prezzo_base in float
df["prezzo_base"] = (
    df["prezzo_base"]
    .replace('[\$,]', '', regex=True)
    .replace('', 0)
    .astype(float)
)

# Inserisce campo coordinate
df["coordinate"] = df.apply(lambda r: f"{r['latitude']},{r['longitude']}", axis=1)
df = df.drop(columns=["latitude", "longitude"])

# === Esportazione JSON ===
df.to_json(OUTPUT_JSON, orient="records", indent=2, force_ascii=False)
print(f"✅ File JSON salvato in: {OUTPUT_JSON}")
