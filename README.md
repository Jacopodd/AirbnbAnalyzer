# AirbnbAnalyzer

Analisi dei dati sugli affitti brevi a Milano tramite MongoDB e Flask.

## 📌 Descrizione

AirbnbAnalyzer è un progetto universitario basato su dati pubblici provenienti dalla piattaforma [Inside Airbnb](https://insideairbnb.com/get-the-data.html). L'obiettivo è analizzare dinamiche di mercato, recensioni e prezzi degli alloggi a Milano, sfruttando un database documentale NoSQL (MongoDB) e un’interfaccia web interattiva sviluppata in Flask.

Il progetto è pensato per soddisfare i requisiti didattici del corso di Basi di Dati 2 (A.A. 2024/2025), tra cui:
- Uso di un DBMS NoSQL (MongoDB)
- Relazioni tra almeno due collezioni tramite attributi condivisi
- Operazioni CRUD complete
- Join tra collezioni e rispetto di vincoli del teorema CAP
- Interfaccia utente minimale per l’interazione

---

## 📁 Dataset

I dati utilizzati sono forniti dal progetto [Inside Airbnb – Milano](https://insideairbnb.com/get-the-data.html). I file da scaricare manualmente e salvare nella cartella `data/` sono:

- `listings.csv`
- `calendar.csv`
- `reviews.csv`
- `neighbourhoods.geojson`

---

## 🧰 Requisiti

- Python 3.10
- MongoDB (installato localmente o accessibile da URI)
- Virtualenv (consigliato)

---

## ⚙️ Setup Ambiente Virtuale

```bash
python3.10 -m venv venv
source venv/bin/activate        # Su Windows: venv\Scripts\activate
pip install flask pymongo pandas
```

---

## 🔄 Pipeline di Preprocessing e Import

### Esecuzione automatica
Per eseguire l’intera pipeline di preprocessing (pulizia, conversione JSON Lines):

```bash
python run_preprocessing.py
```

Questo esegue:
- `preprocessing/preprocess_listings.py`
- `preprocessing/preprocess_calendar.py`
- `preprocessing/preprocess_review.py`
- `preprocessing/preprocess_neighbourhoods.py`
- `convert_all_to_json_lines.py`

### Import in MongoDB
Dopo il preprocessing, importa i file JSON nella base di dati:

```bash
python import_mongo.py
```

Per creare la collezione `host` automaticamente da `alloggi`:

```bash
python extrapolate_hosts.py
```

---

## ☁️ Connessione al Database

La connessione è gestita dal file `db.py`, che accede al database `airbnbMilano`. Se non imposti una variabile d’ambiente `MONGO_URI`, la connessione predefinita sarà:

```
mongodb://localhost:27017/
```

---

## 🚀 Avvio dell'applicazione

Assicurati che MongoDB sia attivo e i dati siano stati importati, poi lancia:

```bash
python app.py
```

Apri il browser su: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Funzionalità principali

- CRUD su tutte le entità: alloggi, host, recensioni, prezzi
- JOIN tra collezioni con `$lookup` e query geospaziali (`$geoIntersects`)
- Interfaccia web user-friendly basata su Flask
- API per dati geospaziali (GeoJSON)

---

## 📂 Struttura delle cartelle

```
├── app.py                  # Web app Flask
├── db.py                   # Connessione al DB
├── run_preprocessing.py    # Pipeline completa automatica
├── convert_all_to_json_lines.py
├── preprocessing/
│   ├── preprocess_listings.py
│   ├── preprocess_calendar.py
│   ├── preprocess_review.py
│   ├── preprocess_neighbourhoods.py
│   ├── import_mongo.py         # Import JSON Lines
│   ├── extrapolate_hosts.py    # Crea collezione 'host'
├── crud/
│   ├── crud_alloggi.py
│   ├── crud_host.py
│   ├── crud_prezzi.py
│   ├── crud_recensioni.py
├── relazioni/
│   ├── alloggi_recensioni.py
│   ├── alloggi_prezzi.py
│   ├── host_alloggi.py
│   ├── alloggi_quartieri.py
├── data/                   # CSV e GeoJSON originali
├── static/                 # Assets (immagini, css, ecc.)
├── ui/                     # Template HTML
```

---

## 📌 Note Finali

- Il progetto è conforme ai requisiti del corso di Basi di Dati 2.
- Sono rispettati due vincoli del teorema CAP: **Availability** e **Partition Tolerance**.
