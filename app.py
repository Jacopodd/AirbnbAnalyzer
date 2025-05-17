from flask import Flask, render_template
from flask import jsonify
from db import get_db_connection

# Inizializza l'app Flask, specificando la cartella dei template
app = Flask(__name__, template_folder="ui", static_folder="static")


# Homepage
@app.route("/")
@app.route("/")
def home():
    db = get_db_connection()
    total_alloggi = db["alloggi"].count_documents({})
    total_host = db["host"].count_documents({})
    total_reviews = db["recensioni"].count_documents({})
    return render_template("home.html",
                           total_alloggi=total_alloggi,
                           total_host=total_host,
                           total_reviews=total_reviews)


# Esempio placeholder: pagina lista alloggi
@app.route("/alloggi")
def lista_alloggi():
    db = get_db_connection()
    alloggi = db["alloggi"].find().limit(10)
    return render_template("alloggi.html", alloggi=alloggi)

# Esempio placeholder: pagina form per nuovo alloggio
@app.route("/alloggi/nuovo")
def nuovo_alloggio():
    return render_template("form_alloggio.html")

@app.route("/recensioni")
def lookup_recensioni():
    return "<h2>Qui andrà la pagina delle recensioni (da implementare)</h2>"

@app.route("/host")
def lookup_host():
    return "<h2>Qui andrà la pagina degli host (da implementare)</h2>"


@app.route("/api/alloggi_geo")
def alloggi_geo():
    db = get_db_connection()
    alloggi = db["alloggi"].find(
        {
            "location.coordinates": {"$exists": True},
            "rating": {"$gte": 4.5},
            "recensioni_totali": {"$gte": 20}
        },
        {
            "titolo": 1,
            "location.coordinates": 1,
            "host_id": 1,
            "zona": 1,
            "rating": 1,
            "recensioni_totali": 1,
            "prezzo_base": 1,
            "tipologia_alloggio": 1,
            "tipo_stanza": 1
        }
    ).sort("rating", -1).limit(200)

    geo_data = []
    for a in alloggi:
        coords = a.get("location", {}).get("coordinates")
        if coords and len(coords) == 2:
            geo_data.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": coords
                },
                "properties": {
                    "titolo": a.get("titolo", "Senza titolo"),
                    "zona": a.get("zona", "-"),
                    "rating": a.get("rating", "-"),
                    "recensioni_totali": a.get("recensioni_totali", 0),
                    "prezzo_base": a.get("prezzo_base", "-"),
                    "tipologia_alloggio": a.get("tipologia_alloggio", "-"),
                    "tipo_stanza": a.get("tipo_stanza", "-"),
                    "host_id": a.get("host_id")
                }
            })

    return jsonify({
        "type": "FeatureCollection",
        "features": geo_data
    })



@app.route("/debug")
def debug():
    db = get_db_connection()
    collections = db.list_collection_names()
    sample = db["alloggi"].find_one()
    return {
        "collections": collections,
        "sample_alloggio": sample
    }


# Altri endpoint da aggiungere:
# - /alloggi/<id>
# - /recensioni
# - /host
# - ecc.

# Avvio del server Flask
if __name__ == "__main__":
    app.run(debug=True)

import os
print("STATIC PATH:", os.path.abspath("static/"))

