import subprocess
import os

# Directory contenente gli script
SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "preprocessing")

# Lista degli script da eseguire in ordine
scripts = [
    "preprocess_listings.py",
    "preprocess_calendar.py",
    "preprocess_review.py",
    "preprocess_neighbourhoods.py",
    "../convert_all_to_json_lines.py",
    "import_mongo.py",
    "extrapolate_hosts.py"
]


print("\n=== Avvio pipeline di preprocessing ===\n")

for script in scripts:
    path = os.path.join(SCRIPT_DIR, script) if not script.startswith("../") else script
    print(f"▶️  Esecuzione: {script}")
    result = subprocess.run(["python", path])
    if result.returncode != 0:
        print(f"❌ Errore nell'esecuzione di {script}\n")
        break
    print("✅ Completato\n")

print("=== Preprocessing completato con successo ===")
