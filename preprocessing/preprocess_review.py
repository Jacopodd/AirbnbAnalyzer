import pandas as pd
import json
from pathlib import Path

# === Percorsi relativi ===
INPUT_CSV = "../data/review.csv"
OUTPUT_JSON = "../data/review_cleaned.json"

# === Caricamento ===
df = pd.read_csv(INPUT_CSV)

# === Selezione + rinomina ===
df = df[[
    'listing_id', 'date', 'reviewer_id', 'comments'
]].rename(columns={
    'listing_id': 'id_alloggio',
    'date': 'data',
    'reviewer_id': 'utente_id',
    'comments': 'testo'
})

# === Conversioni tipi ===
df['id_alloggio'] = df['id_alloggio'].astype(str)
df['utente_id'] = df['utente_id'].astype(str)

# Rimuove eventuali valori nulli nel campo testo
df = df[df['testo'].notnull()]

# === Esportazione JSON ===
df.to_json(OUTPUT_JSON, orient="records", indent=2, force_ascii=False)
print(f"✅ Dati preprocessati salvati in: {OUTPUT_JSON}")
