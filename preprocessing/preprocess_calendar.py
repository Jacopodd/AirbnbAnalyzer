import pandas as pd
import json
from pathlib import Path

# === Percorsi relativi ===
INPUT_CSV = "../data/calendar.csv"
OUTPUT_JSON = "../data/calendar_cleaned.json"

# === Caricamento ===
df = pd.read_csv(INPUT_CSV)

# === Selezione + rinomina ===
df = df[[
    'listing_id', 'date', 'available', 'price'
]].rename(columns={
    'listing_id': 'id_alloggio',
    'date': 'data',
    'available': 'disponibile',
    'price': 'prezzo_giornaliero'
})

# === Conversioni tipi ===
df['id_alloggio'] = df['id_alloggio'].astype(str)

# Converti 't'/'f' → True/False
df['disponibile'] = df['disponibile'].map({'t': True, 'f': False})

# Rimuove il simbolo $ e converte in float
df['prezzo_giornaliero'] = (
    df['prezzo_giornaliero']
    .replace('[\\$,]', '', regex=True)
    .replace('', 0)
    .astype(float)
)

# === Esportazione JSON ===
df.to_json(OUTPUT_JSON, orient="records", indent=2, force_ascii=False)
print(f"✅ Dati preprocessati salvati in: {OUTPUT_JSON}")
