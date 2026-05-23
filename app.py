"""
Application de recherche de voyages
Backend Flask avec intégration Skyscanner RapidAPI + Booking.com
Réseau affilié : Travelpayout (ID 731169)
"""

from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, date
import os

app = Flask(__name__)

# ─────────────────────────────────────────────
#  CONFIGURATION TRAVELPAYOUT + RAPIDAPI
# ─────────────────────────────────────────────
SKYSCANNER_API_KEY  = os.getenv("SKYSCANNER_API_KEY", "VOTRE_CLE_RAPIDAPI_SKYSCANNER")
BOOKING_API_KEY     = os.getenv("BOOKING_API_KEY",    "VOTRE_CLE_RAPIDAPI_BOOKING")

# Travelpayout — votre ID affilié unique
TRAVELPAYOUT_ID     = "731169"

# Codes affiliés Travelpayout (générés automatiquement avec votre ID)
AFF_SKYSCANNER      = TRAVELPAYOUT_ID   # marker ID pour Skyscanner via Travelpayout
AFF_BOOKING         = TRAVELPAYOUT_ID   # marker ID pour Booking via Travelpayout

SKYSCANNER_HOST = "skyscanner50.p.rapidapi.com"
BOOKING_HOST    = "booking-com15.p.rapidapi.com"

# ─────────────────────────────────────────────
#  DONNÉES STATIQUES
# ─────────────────────────────────────────────
VILLES_DEPART = [
    {"nom": "Paris",     "pays": "France",    "flag": "🇫🇷", "iata": "CDG"},
    {"nom": "Lyon",      "pays": "France",    "flag": "🇫🇷", "iata": "LYS"},
    {"nom": "Marseille", "pays": "France",    "flag": "🇫🇷", "iata": "MRS"},
    {"nom": "Bruxelles", "pays": "Belgique",  "flag": "🇧🇪", "iata": "BRU"},
    {"nom": "Genève",    "pays": "Suisse",    "flag": "🇨🇭", "iata": "GVA"},
    {"nom": "Montréal",  "pays": "Canada",    "flag": "🇨🇦", "iata": "YUL"},
    {"nom": "Phuket",    "pays": "Thaïlande", "flag": "🇹🇭", "iata": "HKT"},
]

DESTINATIONS = [
    {"flag":"🇯🇵","nom":"Tokyo",           "pays":"Japon",           "iata":"TYO","booking_id":"Tokyo",          "tags":["Culture","Gastronomie","Modernité"],   "prix_base":2200},
    {"flag":"🇧🇷","nom":"Rio de Janeiro",  "pays":"Brésil",          "iata":"GIG","booking_id":"Rio de Janeiro", "tags":["Plage","Fête","Nature"],               "prix_base":1800},
    {"flag":"🇹🇭","nom":"Chiang Mai",      "pays":"Thaïlande",       "iata":"CNX","booking_id":"Chiang Mai",     "tags":["Temples","Nature","Détente"],          "prix_base":950},
    {"flag":"🇲🇻","nom":"Malé",            "pays":"Maldives",        "iata":"MLE","booking_id":"Male",           "tags":["Luxe","Plage","Snorkeling"],           "prix_base":4500},
    {"flag":"🇵🇪","nom":"Cusco",           "pays":"Pérou",           "iata":"LIM","booking_id":"Cusco",          "tags":["Aventure","Histoire","Randonnée"],     "prix_base":2600},
    {"flag":"🇮🇸","nom":"Reykjavik",       "pays":"Islande",         "iata":"KEF","booking_id":"Reykjavik",      "tags":["Aurores","Nature","Volcans"],          "prix_base":2100},
    {"flag":"🇰🇪","nom":"Nairobi",         "pays":"Kenya",           "iata":"NBO","booking_id":"Nairobi",        "tags":["Safari","Faune","Savane"],             "prix_base":3200},
    {"flag":"🇳🇿","nom":"Queenstown",      "pays":"Nv-Zélande",      "iata":"ZQN","booking_id":"Queenstown",     "tags":["Aventure","Paysages","Sport"],         "prix_base":5200},
    {"flag":"🇲🇦","nom":"Marrakech",       "pays":"Maroc",           "iata":"RAK","booking_id":"Marrakech",      "tags":["Souk","Culture","Désert"],             "prix_base":800},
    {"flag":"🇺🇸","nom":"New York",        "pays":"États-Unis",      "iata":"JFK","booking_id":"New York City",  "tags":["Ville","Shopping","Culture"],          "prix_base":2900},
    {"flag":"🇮🇩","nom":"Bali",            "pays":"Indonésie",       "iata":"DPS","booking_id":"Bali",           "tags":["Spiritualité","Plage","Jungle"],       "prix_base":1400},
    {"flag":"🇬🇷","nom":"Santorin",        "pays":"Grèce",           "iata":"JTR","booking_id":"Santorini",      "tags":["Romance","Mer","Gastronomie"],         "prix_base":1600},
    {"flag":"🇻🇳","nom":"Hanoï",           "pays":"Vietnam",         "iata":"HAN","booking_id":"Hanoi",          "tags":["Rue","Histoire","Gastronomie"],        "prix_base":1100},
    {"flag":"🇿🇦","nom":"Le Cap",          "pays":"Afrique du Sud",  "iata":"CPT","booking_id":"Cape Town",      "tags":["Nature","Vignobles","Mer"],            "prix_base":2400},
    {"flag":"🇦🇷","nom":"Buenos Aires",    "pays":"Argentine",       "iata":"EZE","booking_id":"Buenos Aires",   "tags":["Tango","Gastronomie","Culture"],       "prix_base":2000},
    {"flag":"🇵🇹","nom":"Lisbonne",        "pays":"Portugal",        "iata":"LIS","booking_id":"Lisbon",         "tags":["Histoire","Fado","Gastronomie"],       "prix_base":700},
]


# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────
def prix_total(prix_base: int, adultes: int, enfants: int, bebes: int) -> int:
    """Calcule le prix total en fonction des voyageurs."""
    return round(prix_base * adultes + prix_base * 0.70 * enfants + prix_base * 0.10 * bebes)


def build_skyscanner_url(orig: str, dest: str, d1: str, d2: str,
                          adultes: int, enfants: int, bebes: int) -> str:
    """
    URL affiliée Skyscanner via Travelpayout (marker=731169).
    Redirige via tp.media qui track la commission automatiquement.
    """
    import urllib.parse
    fmt = lambda d: d.replace("-", "")
    target = (
        f"https://www.skyscanner.fr/transport/vols/"
        f"{orig.lower()}/{dest.lower()}/{fmt(d1)}/{fmt(d2)}/"
        f"?adults={adultes}&children={enfants}&infants={bebes}"
    )
    encoded = urllib.parse.quote(target, safe='')
    return (
        f"https://tp.media/r"
        f"?marker={TRAVELPAYOUT_ID}"
        f"&trs=233854"
        f"&p=4114"
        f"&u={encoded}"
        f"&campaign_id=200"
    )


def build_booking_url(destination: str, d1: str, d2: str,
                       adultes: int, enfants: int) -> str:
    """
    URL affiliée Booking.com via Travelpayout (marker=731169).
    """
    import urllib.parse
    dest_enc = urllib.parse.quote(destination)
    target = (
        f"https://www.booking.com/searchresults.fr.html"
        f"?ss={dest_enc}&checkin={d1}&checkout={d2}"
        f"&group_adults={adultes}&group_children={enfants}"
        f"&no_rooms=1"
    )
    encoded = urllib.parse.quote(target, safe='')
    return (
        f"https://tp.media/r"
        f"?marker={TRAVELPAYOUT_ID}"
        f"&trs=233854"
        f"&p=4"
        f"&u={encoded}"
        f"&campaign_id=200"
    )


# ─────────────────────────────────────────────
#  APPEL SKYSCANNER API (RapidAPI)
# ─────────────────────────────────────────────
def get_skyscanner_prices(orig_iata: str, dest_iata: str,
                           d1: str, d2: str, adultes: int) -> dict | None:
    """
    Interroge l'API Skyscanner via RapidAPI pour obtenir le prix réel du vol.
    Retourne un dict avec 'price' et 'currency', ou None si indisponible.
    """
    url = f"https://{SKYSCANNER_HOST}/api/v1/flights/searchFlights"
    headers = {
        "X-RapidAPI-Key":  SKYSCANNER_API_KEY,
        "X-RapidAPI-Host": SKYSCANNER_HOST,
    }
    params = {
        "originSkyId":         orig_iata,
        "destinationSkyId":    dest_iata,
        "originEntityId":      orig_iata,
        "destinationEntityId": dest_iata,
        "date":                d1,
        "returnDate":          d2,
        "adults":              adultes,
        "currency":            "EUR",
        "locale":              "fr-FR",
        "market":              "FR",
        "countryCode":         "FR",
        "cabinClass":          "economy",
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        itineraries = (data.get("data", {})
                           .get("itineraries", {})
                           .get("results", []))
        if itineraries:
            prices = [
                it["price"]["raw"]
                for it in itineraries
                if it.get("price", {}).get("raw")
            ]
            if prices:
                return {"price": round(min(prices)), "currency": "EUR", "source": "live"}
    except Exception as e:
        app.logger.warning(f"Skyscanner API error ({dest_iata}): {e}")
    return None


# ─────────────────────────────────────────────
#  APPEL BOOKING API (RapidAPI)
# ─────────────────────────────────────────────
def get_booking_hotel_price(destination: str, d1: str, d2: str,
                             adultes: int, nuits: int) -> dict | None:
    """
    Interroge l'API Booking via RapidAPI pour obtenir le prix nuit moyen.
    Retourne un dict avec 'price_per_night', ou None si indisponible.
    """
    search_url = f"https://{BOOKING_HOST}/api/v1/hotels/searchDestination"
    headers = {
        "X-RapidAPI-Key":  BOOKING_API_KEY,
        "X-RapidAPI-Host": BOOKING_HOST,
    }
    try:
        r1 = requests.get(search_url, headers=headers,
                          params={"query": destination}, timeout=6)
        r1.raise_for_status()
        results = r1.json().get("data", [])
        if not results:
            return None
        dest_id   = results[0]["dest_id"]
        dest_type = results[0]["dest_type"]

        hotels_url = f"https://{BOOKING_HOST}/api/v1/hotels/searchHotels"
        params2 = {
            "dest_id":        dest_id,
            "search_type":    dest_type,
            "arrival_date":   d1,
            "departure_date": d2,
            "adults":         adultes,
            "room_qty":       1,
            "currency_code":  "EUR",
            "languagecode":   "fr",
            "sort_by":        "popularity",
        }
        r2 = requests.get(hotels_url, headers=headers, params=params2, timeout=8)
        r2.raise_for_status()
        hotels = r2.json().get("data", {}).get("hotels", [])
        if hotels:
            prices = [
                h["property"]["priceBreakdown"]["grossPrice"]["value"]
                for h in hotels[:10]
                if h.get("property", {})
                    .get("priceBreakdown", {})
                    .get("grossPrice", {})
                    .get("value")
            ]
            if prices:
                avg = round(sum(prices) / len(prices) / nuits)
                return {"price_per_night": avg, "source": "live"}
    except Exception as e:
        app.logger.warning(f"Booking API error ({destination}): {e}")
    return None


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
                           villes=VILLES_DEPART,
                           travelpayout_id=TRAVELPAYOUT_ID)


@app.route("/search", methods=["POST"])
def search():
    """
    Endpoint principal de recherche.
    Reçoit les paramètres en JSON et retourne les destinations filtrées.
    """
    data = request.get_json()

    budget  = int(data.get("budget", 3000))
    depart  = data.get("depart", "CDG")
    d1      = data.get("date_depart")
    d2      = data.get("date_retour")
    adultes = max(1, int(data.get("adultes", 2)))
    enfants = max(0, int(data.get("enfants", 0)))
    bebes   = max(0, int(data.get("bebes", 0)))
    fav     = data.get("destination_favorite", "").lower().strip()

    if not d1 or not d2:
        return jsonify({"error": "Dates manquantes"}), 400

    nuits = (datetime.strptime(d2, "%Y-%m-%d") -
             datetime.strptime(d1, "%Y-%m-%d")).days
    if nuits <= 0:
        return jsonify({"error": "Dates invalides"}), 400

    resultats = []
    for dest in DESTINATIONS:
        prix_est = prix_total(dest["prix_base"], adultes, enfants, bebes)
        if prix_est > budget:
            continue

        score = 0
        if prix_est <= budget * 0.75:
            score += 2
        nom_lower = dest["nom"].lower() + " " + dest["pays"].lower()
        if fav and any(fav in nom_lower or m in fav for m in nom_lower.split()):
            score += 10

        url_sky  = build_skyscanner_url(depart, dest["iata"],
                                         d1, d2, adultes, enfants, bebes)
        url_book = build_booking_url(dest["booking_id"], d1, d2, adultes, enfants)

        resultats.append({
            "flag":           dest["flag"],
            "nom":            dest["nom"],
            "pays":           dest["pays"],
            "tags":           dest["tags"],
            "prix_estime":    prix_est,
            "prix_base":      dest["prix_base"],
            "nuits":          nuits,
            "reste":          budget - prix_est,
            "score":          score,
            "url_skyscanner": url_sky,
            "url_booking":    url_book,
            "is_favorite":    score >= 10,
        })

    resultats.sort(key=lambda x: (-x["score"], x["prix_estime"]))

    return jsonify({
        "resultats": resultats[:12],
        "total":     len(resultats),
        "nuits":     nuits,
        "voyageurs": adultes + enfants + bebes,
        "adultes":   adultes,
        "enfants":   enfants,
        "bebes":     bebes,
    })


@app.route("/live-price", methods=["POST"])
def live_price():
    """
    Récupère les prix en temps réel depuis Skyscanner et Booking.
    """
    data    = request.get_json()
    orig    = data.get("orig_iata")
    dest    = data.get("dest_iata")
    booking = data.get("booking_id")
    d1      = data.get("date_depart")
    d2      = data.get("date_retour")
    adultes = int(data.get("adultes", 2))
    enfants = int(data.get("enfants", 0))
    nuits   = int(data.get("nuits", 7))

    sky_data  = get_skyscanner_prices(orig, dest, d1, d2, adultes)
    book_data = get_booking_hotel_price(booking, d1, d2, adultes, nuits)

    return jsonify({"vol": sky_data, "hotel": book_data})


# ─────────────────────────────────────────────
#  LANCEMENT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
