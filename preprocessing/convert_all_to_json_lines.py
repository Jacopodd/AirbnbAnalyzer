import json
import os

# Definizione dei file da convertire
input_output_pairs = {
    "../data/listings_cleaned.json": "../data/listings_cleaned_lines.json",
    "../data/calendar_cleaned.json": "../data/calendar_cleaned_lines.json",
    "../data/review_cleaned.json": "../data/reviews_cleaned_lines.json",
    "../data/neighbourhoods_cleaned.json": "../data/neighbourhoods_cleaned_lines.json"
}

def convert_array_json_to_lines(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"❌ File non trovato: {input_path}")
        return

    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)  # può essere una lista o un dizionario

        with open(output_path, "w", encoding="utf-8") as outfile:
            # Se è un FeatureCollection GeoJSON, estrai le feature
            if isinstance(data, dict) and "features" in data:
                for feature in data["features"]:
                    json.dump(feature, outfile)
                    outfile.write("\n")
            # Altrimenti scrivi ogni elemento della lista su una riga
            elif isinstance(data, list):
                for item in data:
                    json.dump(item, outfile)
                    outfile.write("\n")
            else:
                print(f"⚠️ Formato non riconosciuto in {input_path}")
                return

        print(f"✅ File convertito: {output_path}")

    except json.JSONDecodeError:
        print(f"❌ Errore nel parsing del file: {input_path}")

# Esegui la conversione per tutti i file
for input_path, output_path in input_output_pairs.items():
    convert_array_json_to_lines(input_path, output_path)
