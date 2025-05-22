from datetime import datetime
from uuid import uuid4  # in cima al file

from bson import ObjectId
from flask import Flask, render_template, jsonify, request, redirect, url_for

from crud.crud_host import aggiorna_host, leggi_host, crea_host, lista_host
from crud.crud_prezzi import crea_prezzo, leggi_prezzo, aggiorna_prezzo, elimina_prezzo
from crud.crud_recensioni import leggi_recensione, elimina_recensione, aggiorna_recensione, crea_recensione
from db import get_db_connection
from crud.crud_alloggi import crea_alloggio, aggiorna_alloggio

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


# ALLOGGI -------------------------------------------------------------
@app.route("/alloggi")
def lista_alloggi():
    db = get_db_connection()
    PER_PAGE = 20
    page = int(request.args.get('page', 1))
    skip = (page - 1) * PER_PAGE

    total_alloggi = db["alloggi"].count_documents({})
    alloggi = list(db["alloggi"].find().sort("data_inserimento", -1).skip(skip).limit(PER_PAGE))

    return render_template(
        "lista_alloggi.html",
        alloggi=alloggi,
        page=page,
        total_pages=(total_alloggi + PER_PAGE - 1) // PER_PAGE
    )  # <--- questa parentesi mancava

@app.route("/alloggi/<string:alloggio_id>")
def dettaglio_alloggio(alloggio_id):
    db = get_db_connection()

    # Non serve più usare ObjectId
    alloggio = db["alloggi"].find_one({"_id": alloggio_id})
    if not alloggio:
        return "<h2>Alloggio non trovato</h2>", 404

    # Host
    host = db["host"].find_one({"_id": alloggio["host_id"]})

    # Quartiere (geospaziale)
    quartiere = db["quartieri"].find_one({
        "geometry": {"$geoIntersects": {"$geometry": alloggio["location"]}}
    })

    # Prezzi
    prezzi = list(db["prezzi"].find({"id_alloggio": alloggio_id}).sort("data", -1).limit(5))

    # ✅ Converti le date se sono stringhe
    for p in prezzi:
        if isinstance(p["data"], str):
            try:
                p["data"] = datetime.fromisoformat(p["data"])
            except Exception:
                p["data"] = None

    # Recensioni
    recensioni = list(db["recensioni"].find({"id_alloggio": alloggio_id}).sort("data", -1).limit(5))

    return render_template(
        "dettaglio_alloggio.html",
        alloggio=alloggio,
        host=host,
        quartiere=quartiere,
        prezzi=prezzi,
        recensioni=recensioni
    )

@app.route("/alloggi/nuovo", methods=["GET", "POST"])
def crea_alloggio_route():
    db = get_db_connection()

    if request.method == "POST":
        form = request.form

        alloggio = {
            "_id": str(uuid4()),
            "titolo": form["titolo"],
            "host_id": form["host_id"],
            "host_nome": form["host_nome"],
            "zona": form["zona"],
            "tipo_stanza": form.get("tipo_stanza", ""),
            "tipologia_alloggio": form.get("tipologia_alloggio", ""),
            "prezzo_base": float(form["prezzo_base"]) if form.get("prezzo_base") else None,
            "min_notti": int(form["min_notti"]) if form.get("min_notti") else None,
            "max_notti": int(form["max_notti"]) if form.get("max_notti") else None,
            "posti_letto": int(form["posti_letto"]) if form.get("posti_letto") else None,
            "camere": int(form["camere"]) if form.get("camere") else None,
            "letti": int(form["letti"]) if form.get("letti") else None,
            "bagni_descrizione": form.get("bagni_descrizione", ""),
            "servizi": [s.strip() for s in form.get("servizi", "").split(",") if s.strip()],
            "disponibilita_annuale": int(form["disponibilita_annuale"]) if form.get("disponibilita_annuale") else None,
            "recensioni_totali": int(form["recensioni_totali"]) if form.get("recensioni_totali") else None,
            "ultima_recensione": datetime.strptime(form["ultima_recensione"], "%Y-%m-%d") if form.get("ultima_recensione") else None,
            "recensioni_mensili": float(form["recensioni_mensili"]) if form.get("recensioni_mensili") else None,
            "rating": float(form["rating"]) if form.get("rating") else None,
            "prenotazione_immediata": form.get("prenotazione_immediata") == "true",
            "data_inserimento": datetime.utcnow()
        }

        if form.get("coordinate"):
            try:
                lat, lon = [float(x.strip()) for x in form["coordinate"].split(",")]
                alloggio["location"] = {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            except Exception as e:
                print("⚠️ Errore parsing coordinate:", e)

        crea_alloggio(db, alloggio)
        return redirect(url_for("lista_alloggi"))

    # GET → carica i primi 100 host
    host_limited = list(db["host"].find().sort("data_inserimento", -1).limit(100))
    return render_template("aggiungi_alloggio.html", host_limited=host_limited)


@app.route("/alloggi/<string:alloggio_id>/modifica", methods=["GET", "POST"])
def modifica_alloggio(alloggio_id):
    db = get_db_connection()

    if request.method == "POST":
        form = request.form
        aggiornamenti = {
            "titolo": form["titolo"],
            "host_id": form["host_id"],
            "host_nome": form["host_nome"],
            "zona": form["zona"],
            "prezzo_base": float(form["prezzo_base"]) if form.get("prezzo_base") else None
        }
        aggiorna_alloggio(db, alloggio_id, aggiornamenti)
        return redirect(url_for("dettaglio_alloggio", alloggio_id=alloggio_id))

    # GET → mostra form precompilato
    alloggio = db["alloggi"].find_one({"_id": alloggio_id})
    if not alloggio:
        return "Alloggio non trovato", 404

    host_limited = list(db["host"].find().sort("data_inserimento", -1).limit(100))
    return render_template("modifica_alloggio.html", alloggio=alloggio, host_limited=host_limited)


@app.route("/alloggi/<string:alloggio_id>/elimina", methods=["POST"])
def elimina_alloggio(alloggio_id):
    db = get_db_connection()
    try:
        result = db["alloggi"].delete_one({"_id": ObjectId(alloggio_id)})
        print(f"🗑️ Eliminato {result.deleted_count} documento")
    except Exception as e:
        print("Errore durante l'eliminazione:", e)
    return redirect(url_for("lista_alloggi"))


# RECENSIONI -------------------------------------------
@app.route("/alloggi/<string:alloggio_id>/recensioni")
def visualizza_recensioni(alloggio_id):
    db = get_db_connection()

    alloggio = db["alloggi"].find_one({"_id": alloggio_id})
    if not alloggio:
        return "Alloggio non trovato", 404

    recensioni = list(
        db["recensioni"].find({"id_alloggio": alloggio_id}).sort("data", -1)
    )

    # Converti la data se è una stringa
    for rec in recensioni:
        if isinstance(rec["data"], str):
            try:
                rec["data"] = datetime.fromisoformat(rec["data"])
            except Exception:
                rec["data"] = None

    return render_template("lista_recensioni.html", alloggio=alloggio, recensioni=recensioni)

@app.route("/recensioni/nuova/<string:alloggio_id>", methods=["GET", "POST"])
def nuova_recensione(alloggio_id):
    db = get_db_connection()
    if request.method == "POST":
        form = request.form
        nuova = {
            "id_alloggio": alloggio_id,
            "data": datetime.strptime(form["data"], "%Y-%m-%d"),
            "utente_id": form["utente_id"],
            "testo": form["testo"]
        }
        crea_recensione(db, nuova)
        return redirect(url_for("dettaglio_alloggio", alloggio_id=alloggio_id))
    return render_template("nuova_recensione.html", alloggio_id=alloggio_id)

@app.route("/recensioni/<string:recensione_id>/modifica", methods=["GET", "POST"])
def modifica_recensione(recensione_id):
    db = get_db_connection()
    recensione = leggi_recensione(db, recensione_id)
    if not recensione:
        return "Recensione non trovata", 404
    if request.method == "POST":
        form = request.form
        aggiorna_recensione(db, recensione_id, {
            "data": datetime.strptime(form["data"], "%Y-%m-%d"),
            "testo": form["testo"]
        })
        return redirect(url_for("dettaglio_alloggio", alloggio_id=recensione["id_alloggio"]))
    return render_template("modifica_recensione.html", recensione=recensione)

@app.route("/recensioni/<string:recensione_id>/elimina", methods=["POST"])
def elimina_recensione_route(recensione_id):
    db = get_db_connection()
    recensione = leggi_recensione(db, recensione_id)
    if recensione:
        elimina_recensione(db, recensione_id)
        return redirect(url_for("dettaglio_alloggio", alloggio_id=recensione["id_alloggio"]))
    return "Recensione non trovata", 404


# PREZZO --------------------------------------------------
@app.route("/prezzi/nuovo/<string:alloggio_id>", methods=["GET", "POST"])
def nuovo_prezzo(alloggio_id):
    db = get_db_connection()
    if request.method == "POST":
        form = request.form
        prezzo = {
            "id_alloggio": alloggio_id,
            "data": datetime.strptime(form["data"], "%Y-%m-%d"),
            "prezzo_giornaliero": float(form["prezzo_giornaliero"])
        }
        crea_prezzo(db, prezzo)
        return redirect(url_for("dettaglio_alloggio", alloggio_id=alloggio_id))
    return render_template("nuovo_prezzo.html", alloggio_id=alloggio_id)

@app.route("/prezzi/<string:prezzo_id>/modifica", methods=["GET", "POST"])
def modifica_prezzo(prezzo_id):
    db = get_db_connection()
    prezzo = leggi_prezzo(db, prezzo_id)
    if not prezzo:
        return "Prezzo non trovato", 404
    if request.method == "POST":
        form = request.form
        aggiornamenti = {
            "data": datetime.strptime(form["data"], "%Y-%m-%d"),
            "prezzo_giornaliero": float(form["prezzo_giornaliero"])
        }
        aggiorna_prezzo(db, prezzo_id, aggiornamenti)
        return redirect(url_for("dettaglio_alloggio", alloggio_id=prezzo["id_alloggio"]))
    return render_template("modifica_prezzo.html", prezzo=prezzo)

@app.route("/prezzi/<string:prezzo_id>/elimina", methods=["POST"])
def elimina_prezzo_route(prezzo_id):
    db = get_db_connection()
    prezzo = leggi_prezzo(db, prezzo_id)
    if prezzo:
        elimina_prezzo(db, prezzo_id)
        return redirect(url_for("dettaglio_alloggio", alloggio_id=prezzo["id_alloggio"]))
    return "Prezzo non trovato", 404


# HOST ----------------------------------------------------
@app.route("/host")
def lista_host_view():
    db = get_db_connection()

    PER_PAGE = 12
    page = int(request.args.get("page", 1))
    skip = (page - 1) * PER_PAGE

    # Carico solo gli host della pagina attuale
    host = list(
        db["host"]
        .find()
        .sort("data_inserimento", -1)
        .skip(skip)
        .limit(PER_PAGE)
    )

    # Creo una lista di ID da cercare
    host_ids = [h["_id"] for h in host]

    # Conto gli alloggi per ciascun host
    pipeline = [
        { "$match": { "host_id": { "$in": host_ids } } },
        { "$group": { "_id": "$host_id", "count": { "$sum": 1 } } }
    ]
    counts = {doc["_id"]: doc["count"] for doc in db["alloggi"].aggregate(pipeline)}

    # Assegno il conteggio a ogni host
    for h in host:
        h["num_alloggi"] = counts.get(h["_id"], 0)

    total_host = db["host"].count_documents({})

    return render_template(
        "lista_host.html",
        host=host,
        page=page,
        total_pages=(total_host + PER_PAGE - 1) // PER_PAGE
    )



@app.route("/host/nuovo", methods=["GET", "POST"])
def nuovo_host():
    db = get_db_connection()
    if request.method == "POST":
        form = request.form
        host = {
            "_id": str(uuid4()),
            "nome": form["nome"],
            "data_inserimento": datetime.utcnow()
        }
        crea_host(db, host)
        return redirect(url_for("lista_host_view"))
    return render_template("nuovo_host.html")

@app.route("/host/<string:host_id>/modifica", methods=["GET", "POST"])
def modifica_host(host_id):
    db = get_db_connection()
    host = leggi_host(db, host_id)
    if not host:
        return "Host non trovato", 404
    if request.method == "POST":
        form = request.form
        aggiornamenti = {
            "nome": form["nome"]
        }
        aggiorna_host(db, host_id, aggiornamenti)
        return redirect(url_for("lista_host_view"))
    return render_template("modifica_host.html", host=host)


@app.route("/host/<string:host_id>/elimina", methods=["POST"])
def elimina_host(host_id):
    db = get_db_connection()
    elimina_host(db, host_id)
    return redirect(url_for("lista_host"))


@app.route("/host/<string:host_id>")
def dettaglio_host(host_id):
    db = get_db_connection()

    # Trova l'host specifico
    host_base = db["host"].find_one({"_id": host_id})
    if not host_base:
        return "Host non trovato", 404

    # Esegui lookup per unire alloggi
    pipeline = [
        {"$match": {"_id": host_id}},
        {"$lookup": {
            "from": "alloggi",
            "localField": "_id",
            "foreignField": "host_id",
            "as": "alloggi_gestiti"
        }}
    ]
    risultati = list(db["host"].aggregate(pipeline))
    host_dettagliato = risultati[0] if risultati else {}

    # 🔁 Reintegra i campi base eventualmente mancanti
    host_dettagliato.setdefault("data_inserimento", host_base.get("data_inserimento"))
    host_dettagliato.setdefault("nome", host_base.get("nome"))

    return render_template("dettaglio_host.html", host=host_dettagliato)

@app.route("/quartiere/<string:alloggio_id>")
def dettaglio_quartiere_alloggio(alloggio_id):
    db = get_db_connection()

    alloggio = db["alloggi"].find_one({"_id": alloggio_id})
    if not alloggio:
        return "Alloggio non trovato", 404

    # Esegui join geospaziale per trovare il quartiere
    quartiere = db["quartieri"].find_one({
        "geometry": {
            "$geoIntersects": {
                "$geometry": alloggio.get("location", {})
            }
        }
    })

    # Estraggo nome quartiere (se esiste)
    nome_quartiere = "-"
    if quartiere:
        nome_quartiere = quartiere.get("properties", {}).get("quartiere") or quartiere.get("neighbourhood")

    return render_template("dettaglio_quartiere.html",
                           alloggio=alloggio,
                           nome_quartiere=nome_quartiere)

@app.route("/prezzi-per-zona")
def prezzi_per_zona():
    db = get_db_connection()

    pipeline = [
        { "$match": { "prezzo_base": { "$ne": None }, "zona": { "$ne": None } } },
        { "$group": {
            "_id": "$zona",
            "media_prezzo": { "$avg": "$prezzo_base" },
            "num_alloggi": { "$sum": 1 }
        }},
        { "$sort": { "media_prezzo": -1 } }
    ]

    risultati = list(db["alloggi"].aggregate(pipeline))

    return render_template("prezzi_per_zona.html", dati=risultati)


# CAMBIO PAGINE -------------------------------------------
@app.route("/alloggi/nuovo")
def nuovo_alloggio():
    return render_template("aggiungi_alloggio.html")

@app.route("/entita/lista")
def lista_entita():
    return render_template("lista_entita.html")

@app.route("/alloggi/<string:alloggio_id>/prezzi")
def lista_prezzi_alloggio(alloggio_id):
    db = get_db_connection()

    alloggio = db["alloggi"].find_one({"_id": alloggio_id})
    if not alloggio:
        return "Alloggio non trovato", 404

    prezzi = list(
        db["prezzi"].find({"id_alloggio": alloggio_id}).sort("data", -1)
    )

    # Conversione delle date
    for p in prezzi:
        if isinstance(p.get("data"), str):
            try:
                p["data"] = datetime.fromisoformat(p["data"])
            except Exception:
                p["data"] = None

    return render_template("lista_prezzi.html", alloggio=alloggio, prezzi=prezzi)




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

