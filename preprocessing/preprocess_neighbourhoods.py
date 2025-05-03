import json
from pathlib import Path

# === Percorsi relativi ===
INPUT_GEOJSON = "../data/neighbourhoods.geojson"
OUTPUT_JSON = "../data/neighbourhoods_cleaned.json"

# === Caricamento GeoJSON ===
with open(INPUT_GEOJSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# === Pulizia ===
for feature in data["features"]:
    props = feature.get("properties", {})
    # Rimuovi 'neighbourhood_group'
    props.pop("neighbourhood_group", None)
    # Lascia solo 'neighbourhood'
    feature["properties"] = {
        "quartiere": props.get("neighbourhood")
    }

# === Salvataggio JSON pulito ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Quartieri salvati in: {OUTPUT_JSON}")
