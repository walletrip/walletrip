"""
Pouch Voyage — Application Streamlit
Travelpayout ID: 731169
"""

import streamlit as st
import requests
import urllib.parse
import math
from datetime import datetime, date, timedelta

st.set_page_config(
    page_title="Pouch Voyage",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@300;400;500&display=swap');
  :root {
    --cream:#F5F0E8; --cream2:#EDE8DE; --ink:#0D0D0D;
    --muted:#6B6560; --border:#D4CFC6; --white:#FEFCF8;
  }
  html,body,[class*="css"]{font-family:'Inter',sans-serif;background-color:var(--cream)!important;color:var(--ink)!important;}
  section[data-testid="stMain"],.main .block-container{background-color:var(--cream)!important;}
  section[data-testid="stSidebar"]{background:var(--white)!important;border-right:1px solid var(--border)!important;}
  div[data-testid="stSidebarContent"]{padding:2rem 1.4rem;}
  header[data-testid="stHeader"]{background:var(--cream)!important;}
  .logo-wrap{display:flex;align-items:center;gap:16px;margin:2rem 0 0.4rem;}
  .main-title{font-family:'Cormorant Garamond',serif;font-size:3rem;font-weight:300;color:var(--ink);letter-spacing:0.02em;line-height:1;}
  .subtitle{font-size:0.88rem;font-weight:300;color:var(--muted);margin-bottom:2rem;letter-spacing:0.03em;}
  .summary-box{background:var(--cream2);border:1px solid var(--border);border-radius:0;padding:0.8rem 1.2rem;margin-bottom:2rem;font-size:0.85rem;color:var(--muted);}
  .summary-box b{color:var(--ink);}
  div[data-testid="stVerticalBlockBorderWrapper"]{border:1px solid var(--border)!important;border-radius:0!important;background:var(--white)!important;padding:0.2rem 0.6rem!important;transition:border-color 0.2s!important;}
  div[data-testid="stVerticalBlockBorderWrapper"]:hover{border-color:var(--ink)!important;}
  div[data-testid="stMetric"]{background:var(--cream2)!important;border:1px solid var(--border)!important;border-radius:0!important;padding:0.6rem 1rem!important;}
  div[data-testid="stMetricValue"]{font-family:'Cormorant Garamond',serif!important;font-size:1.8rem!important;font-weight:400!important;color:var(--ink)!important;}
  div[data-testid="stMetricLabel"]{font-size:0.75rem!important;color:var(--muted)!important;}
  div[data-testid="stLinkButton"] a{background:var(--ink)!important;color:var(--cream)!important;border:1px solid var(--ink)!important;border-radius:0!important;font-size:0.78rem!important;font-weight:400!important;letter-spacing:0.06em;text-transform:uppercase;padding:8px 16px!important;}
  div[data-testid="stLinkButton"] a:hover{background:var(--cream)!important;color:var(--ink)!important;}
  div[data-testid="stButton"] button{background:var(--ink)!important;color:var(--cream)!important;border:1px solid var(--ink)!important;border-radius:0!important;font-size:0.8rem!important;font-weight:400!important;letter-spacing:0.06em;text-transform:uppercase;}
  div[data-testid="stButton"] button:hover{background:var(--cream)!important;color:var(--ink)!important;}
  div[data-testid="stSlider"]>div>div>div{background:var(--ink)!important;}
  div[data-testid="stAlert"]{background:var(--cream2)!important;border:1px solid var(--border)!important;border-radius:0!important;color:var(--ink)!important;font-size:0.83rem!important;}
  div[data-testid="stInfo"]{background:var(--cream2)!important;border-color:var(--border)!important;border-radius:0!important;color:var(--muted)!important;}
  .stCaption,[data-testid="stCaptionContainer"] p{color:var(--muted)!important;}
  section[data-testid="stSidebar"] label{color:var(--ink)!important;font-size:0.82rem!important;}
  hr{border-color:var(--border)!important;}
  .no-result{text-align:center;padding:4rem;color:var(--muted);font-size:0.95rem;font-weight:300;}

  /* Itinéraire backpacker */
  .itin-header{font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:300;color:var(--ink);margin:1.5rem 0 0.3rem;letter-spacing:0.02em;}
  .itin-subtitle{font-size:0.82rem;color:var(--muted);margin-bottom:1.5rem;}
  .itin-step{display:flex;gap:1rem;margin-bottom:0;align-items:stretch;}
  .itin-line{display:flex;flex-direction:column;align-items:center;width:28px;flex-shrink:0;}
  .itin-dot{width:10px;height:10px;border-radius:50%;background:var(--ink);flex-shrink:0;margin-top:5px;}
  .itin-dot-home{width:14px;height:14px;border-radius:50%;border:2px solid var(--ink);background:var(--cream);flex-shrink:0;margin-top:3px;}
  .itin-vline{width:1px;background:var(--border);flex:1;margin:4px 0;}
  .itin-content{padding-bottom:1.4rem;flex:1;}
  .itin-city{font-weight:500;font-size:0.95rem;color:var(--ink);}
  .itin-meta{font-size:0.78rem;color:var(--muted);margin-top:2px;}
  .itin-price{font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:var(--ink);margin-top:4px;}
  .itin-tags{font-size:0.72rem;color:var(--muted);margin-top:3px;}
  .budget-bar-wrap{background:var(--cream2);border:1px solid var(--border);padding:1rem 1.2rem;margin:1.5rem 0;}
  .budget-bar-label{font-size:0.78rem;color:var(--muted);margin-bottom:6px;}
  .budget-bar-bg{background:var(--border);height:4px;border-radius:0;}
  .budget-bar-fill{background:var(--ink);height:4px;}
  .budget-numbers{display:flex;justify-content:space-between;margin-top:5px;font-size:0.78rem;color:var(--ink);}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
TRAVELPAYOUT_ID    = "731169"
SKYSCANNER_API_KEY = st.secrets.get("SKYSCANNER_API_KEY", "")
BOOKING_API_KEY    = st.secrets.get("BOOKING_API_KEY", "")
SKYSCANNER_HOST    = "skyscanner50.p.rapidapi.com"
BOOKING_HOST       = "booking-com15.p.rapidapi.com"

# ─────────────────────────────────────────────
#  TRADUCTIONS
# ─────────────────────────────────────────────
LANGS = {
    "🇫🇷 Français": {
        "subtitle":"Trouvez votre prochaine aventure selon votre budget",
        "tab_dest":"Destinations","tab_back":"Backpacker",
        "depart":"Ville de départ","dates":"Dates du voyage",
        "budget":"Budget total (€)","budget_sel":"Budget : {b:,} €",
        "voyageurs":"Voyageurs","adultes":"Adultes","enfants":"Enfants","bebes":"Bébés",
        "nb_dest":"Nombre de destinations (backpacker)","duree_label":"durée",
        "fav":"Destination préférée (optionnel)","fav_ph":"ex : Tokyo, Bali…",
        "search":"Rechercher","powered":"Propulsé par Travelpayout",
        "fill_form":"Remplissez le formulaire et cliquez sur Rechercher.",
        "date_err":"La date de retour doit être après la date de départ.",
        "found":"{n} destination(s) · {nuits} nuit(s) · {v} voyageur(s) · Budget {b:,} €",
        "no_result":"Aucune destination dans ce budget. Essayez d'augmenter le budget.",
        "price_live":"Vol (prix en direct)","price_est":"Prix de départ estimé",
        "price_help":"Indicatif — cliquez Skyscanner pour le prix exact.",
        "hotel_live":"Hôtel : ~{p:,} €/nuit","reste":"Budget restant : {r:,} € — {n} nuits",
        "btn_sky":"Skyscanner","btn_book":"Booking","fav_label":"Favori",
        "back_title":"Votre circuit backpacker","back_sub":"Itinéraire optimisé · {n} étapes · {nuits} nuits au total",
        "back_depart":"Départ","back_retour":"Retour",
        "back_nuits":"{n} nuits","back_vol":"Vol estimé","back_hotel":"Hôtel ~{p} €/nuit",
        "back_budget_used":"Budget utilisé","back_budget_rest":"Reste",
        "back_no":"Pas assez de destinations dans ce budget pour un circuit backpacker.",
        "back_btn_sky":"Réserver ce vol","back_btn_book":"Trouver un hôtel",
        "nuits_label":"nuits par étape",
    },
    "🇬🇧 English": {
        "subtitle":"Find your next adventure within your budget",
        "tab_dest":"Destinations","tab_back":"Backpacker",
        "depart":"Departure city","dates":"Travel dates",
        "budget":"Total budget (€)","budget_sel":"Budget: €{b:,}",
        "voyageurs":"Travellers","adultes":"Adults","enfants":"Children","bebes":"Infants",
        "nb_dest":"Number of stops (backpacker)","duree_label":"duration",
        "fav":"Preferred destination (optional)","fav_ph":"e.g. Tokyo, Bali…",
        "search":"Search","powered":"Powered by Travelpayout",
        "fill_form":"Fill in the form and click Search.",
        "date_err":"Return date must be after departure date.",
        "found":"{n} destination(s) · {nuits} night(s) · {v} traveller(s) · Budget €{b:,}",
        "no_result":"No destinations in this budget. Try increasing it.",
        "price_live":"Flight (live price)","price_est":"Estimated price",
        "price_help":"Indicative — click Skyscanner for exact price.",
        "hotel_live":"Hotel: ~€{p:,}/night","reste":"Remaining: €{r:,} — {n} nights",
        "btn_sky":"Skyscanner","btn_book":"Booking","fav_label":"Favourite",
        "back_title":"Your backpacker route","back_sub":"Optimised itinerary · {n} stops · {nuits} nights total",
        "back_depart":"Departure","back_retour":"Return",
        "back_nuits":"{n} nights","back_vol":"Est. flight","back_hotel":"Hotel ~€{p}/night",
        "back_budget_used":"Budget used","back_budget_rest":"Remaining",
        "back_no":"Not enough destinations in this budget for a backpacker route.",
        "back_btn_sky":"Book this flight","back_btn_book":"Find a hotel",
        "nuits_label":"nights per stop",
    },
    "🇪🇸 Español": {
        "subtitle":"Encuentra tu próxima aventura según tu presupuesto",
        "tab_dest":"Destinos","tab_back":"Mochilero",
        "depart":"Ciudad de salida","dates":"Fechas del viaje",
        "budget":"Presupuesto total (€)","budget_sel":"Presupuesto: {b:,} €",
        "voyageurs":"Viajeros","adultes":"Adultos","enfants":"Niños","bebes":"Bebés",
        "nb_dest":"Número de destinos (mochilero)","duree_label":"duración",
        "fav":"Destino preferido (opcional)","fav_ph":"ej: Tokio, Bali…",
        "search":"Buscar","powered":"Desarrollado por Travelpayout",
        "fill_form":"Rellena el formulario y haz clic en Buscar.",
        "date_err":"La fecha de regreso debe ser posterior a la de salida.",
        "found":"{n} destino(s) · {nuits} noche(s) · {v} viajero(s) · Presupuesto {b:,} €",
        "no_result":"Ningún destino en este presupuesto. Intenta aumentarlo.",
        "price_live":"Vuelo (precio en directo)","price_est":"Precio estimado",
        "price_help":"Indicativo — haz clic en Skyscanner para el precio exacto.",
        "hotel_live":"Hotel: ~{p:,} €/noche","reste":"Restante: {r:,} € — {n} noches",
        "btn_sky":"Skyscanner","btn_book":"Booking","fav_label":"Favorito",
        "back_title":"Tu ruta mochilera","back_sub":"Itinerario optimizado · {n} paradas · {nuits} noches en total",
        "back_depart":"Salida","back_retour":"Regreso",
        "back_nuits":"{n} noches","back_vol":"Vuelo estimado","back_hotel":"Hotel ~{p} €/noche",
        "back_budget_used":"Presupuesto usado","back_budget_rest":"Restante",
        "back_no":"No hay suficientes destinos en este presupuesto para una ruta mochilera.",
        "back_btn_sky":"Reservar este vuelo","back_btn_book":"Buscar hotel",
        "nuits_label":"noches por etapa",
    },
}

# ─────────────────────────────────────────────
#  DONNÉES
# ─────────────────────────────────────────────
VILLES_DEPART = [
    {"nom":"Paris",    "pays":"France",    "flag":"🇫🇷","iata":"CDG","lat":48.85,"lng":2.35},
    {"nom":"Lyon",     "pays":"France",    "flag":"🇫🇷","iata":"LYS","lat":45.75,"lng":4.83},
    {"nom":"Marseille","pays":"France",    "flag":"🇫🇷","iata":"MRS","lat":43.30,"lng":5.38},
    {"nom":"Bruxelles","pays":"Belgique",  "flag":"🇧🇪","iata":"BRU","lat":50.85,"lng":4.35},
    {"nom":"Genève",   "pays":"Suisse",    "flag":"🇨🇭","iata":"GVA","lat":46.20,"lng":6.14},
    {"nom":"Montréal", "pays":"Canada",    "flag":"🇨🇦","iata":"YUL","lat":45.50,"lng":-73.57},
    {"nom":"Phuket",   "pays":"Thaïlande", "flag":"🇹🇭","iata":"HKT","lat":7.88,"lng":98.39},
]

DESTINATIONS = [
    {"flag":"🇯🇵","nom":"Tokyo",         "pays":"Japon",         "iata":"TYO","booking_id":"Tokyo",        "tags":["Culture","Gastronomie","Modernité"], "prix_base":2200,"lat":35.68,"lng":139.69,"region":"Asie"},
    {"flag":"🇧🇷","nom":"Rio de Janeiro","pays":"Brésil",        "iata":"GIG","booking_id":"Rio de Janeiro","tags":["Plage","Fête","Nature"],             "prix_base":1800,"lat":-22.90,"lng":-43.17,"region":"Amérique du Sud"},
    {"flag":"🇹🇭","nom":"Bangkok",       "pays":"Thaïlande",     "iata":"BKK","booking_id":"Bangkok",       "tags":["Street food","Temples","Nuit"],      "prix_base":800, "lat":13.75,"lng":100.50,"region":"Asie du Sud-Est"},
    {"flag":"🇹🇭","nom":"Chiang Mai",    "pays":"Thaïlande",     "iata":"CNX","booking_id":"Chiang Mai",   "tags":["Temples","Nature","Détente"],        "prix_base":950, "lat":18.79,"lng":98.98,"region":"Asie du Sud-Est"},
    {"flag":"🇲🇻","nom":"Malé",          "pays":"Maldives",      "iata":"MLE","booking_id":"Male",         "tags":["Luxe","Plage","Snorkeling"],         "prix_base":4500,"lat":4.17,"lng":73.51,"region":"Océan Indien"},
    {"flag":"🇵🇪","nom":"Lima",          "pays":"Pérou",         "iata":"LIM","booking_id":"Lima",         "tags":["Gastronomie","Histoire","Surf"],      "prix_base":1800,"lat":-12.05,"lng":-77.04,"region":"Amérique du Sud"},
    {"flag":"🇮🇸","nom":"Reykjavik",     "pays":"Islande",       "iata":"KEF","booking_id":"Reykjavik",    "tags":["Aurores","Nature","Volcans"],        "prix_base":2100,"lat":64.13,"lng":-21.82,"region":"Europe Nord"},
    {"flag":"🇰🇪","nom":"Nairobi",       "pays":"Kenya",         "iata":"NBO","booking_id":"Nairobi",      "tags":["Safari","Faune","Savane"],           "prix_base":3200,"lat":-1.29,"lng":36.82,"region":"Afrique"},
    {"flag":"🇲🇦","nom":"Marrakech",     "pays":"Maroc",         "iata":"RAK","booking_id":"Marrakech",    "tags":["Souk","Culture","Désert"],           "prix_base":800, "lat":31.63,"lng":-7.99,"region":"Afrique du Nord"},
    {"flag":"🇺🇸","nom":"New York",      "pays":"États-Unis",    "iata":"JFK","booking_id":"New York City","tags":["Ville","Shopping","Culture"],        "prix_base":2900,"lat":40.71,"lng":-74.00,"region":"Amérique du Nord"},
    {"flag":"🇮🇩","nom":"Bali",          "pays":"Indonésie",     "iata":"DPS","booking_id":"Bali",         "tags":["Spiritualité","Plage","Jungle"],     "prix_base":1400,"lat":-8.34,"lng":115.09,"region":"Asie du Sud-Est"},
    {"flag":"🇬🇷","nom":"Santorin",      "pays":"Grèce",         "iata":"JTR","booking_id":"Santorini",    "tags":["Romance","Mer","Gastronomie"],       "prix_base":1600,"lat":36.39,"lng":25.46,"region":"Europe Sud"},
    {"flag":"🇻🇳","nom":"Hanoï",         "pays":"Vietnam",       "iata":"HAN","booking_id":"Hanoi",        "tags":["Rue","Histoire","Gastronomie"],      "prix_base":900, "lat":21.03,"lng":105.85,"region":"Asie du Sud-Est"},
    {"flag":"🇻🇳","nom":"Ho Chi Minh",   "pays":"Vietnam",       "iata":"SGN","booking_id":"Ho Chi Minh City","tags":["Énergie","Gastronomie","Histoire"],"prix_base":850,"lat":10.82,"lng":106.63,"region":"Asie du Sud-Est"},
    {"flag":"🇲🇾","nom":"Kuala Lumpur",  "pays":"Malaisie",      "iata":"KUL","booking_id":"Kuala Lumpur", "tags":["Moderne","Street food","Shopping"],  "prix_base":750, "lat":3.14,"lng":101.69,"region":"Asie du Sud-Est"},
    {"flag":"🇸🇬","nom":"Singapour",     "pays":"Singapour",     "iata":"SIN","booking_id":"Singapore",    "tags":["Luxe","Gastronomie","Modernité"],    "prix_base":1000,"lat":1.35,"lng":103.82,"region":"Asie du Sud-Est"},
    {"flag":"🇿🇦","nom":"Le Cap",        "pays":"Afrique du Sud","iata":"CPT","booking_id":"Cape Town",    "tags":["Nature","Vignobles","Mer"],          "prix_base":2400,"lat":-33.93,"lng":18.42,"region":"Afrique"},
    {"flag":"🇦🇷","nom":"Buenos Aires",  "pays":"Argentine",     "iata":"EZE","booking_id":"Buenos Aires", "tags":["Tango","Gastronomie","Culture"],     "prix_base":2000,"lat":-34.61,"lng":-58.38,"region":"Amérique du Sud"},
    {"flag":"🇵🇹","nom":"Lisbonne",      "pays":"Portugal",      "iata":"LIS","booking_id":"Lisbon",       "tags":["Histoire","Fado","Gastronomie"],     "prix_base":700, "lat":38.72,"lng":-9.14,"region":"Europe"},
    {"flag":"🇯🇵","nom":"Osaka",         "pays":"Japon",         "iata":"KIX","booking_id":"Osaka",        "tags":["Street food","Modernité","Culture"],  "prix_base":2000,"lat":34.69,"lng":135.50,"region":"Asie"},
    {"flag":"🇨🇲","nom":"Phnom Penh",    "pays":"Cambodge",      "iata":"PNH","booking_id":"Phnom Penh",   "tags":["Histoire","Temples","Fleuve"],       "prix_base":750, "lat":11.56,"lng":104.92,"region":"Asie du Sud-Est"},
    {"flag":"🇳🇵","nom":"Katmandou",     "pays":"Népal",         "iata":"KTM","booking_id":"Kathmandu",    "tags":["Himalaya","Trek","Spiritualité"],    "prix_base":1100,"lat":27.70,"lng":85.31,"region":"Asie du Sud"},
]

# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────
def prix_total(prix_base, adultes, enfants, bebes):
    return round(prix_base * adultes + prix_base * 0.70 * enfants + prix_base * 0.10 * bebes)

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def build_skyscanner_url(orig, dest, d1, d2, adultes, enfants, bebes):
    fmt = lambda d: d.replace("-","")
    return (
        f"https://www.skyscanner.fr/transport/vols/{orig.lower()}/{dest.lower()}/{fmt(d1)}/{fmt(d2)}/"
        f"?adults={adultes}&children={enfants}&infants={bebes}"
        f"&utm_source=travelpayout&utm_medium=affiliate&utm_campaign={TRAVELPAYOUT_ID}"
    )

def build_booking_url(destination, d1, d2, adultes, enfants):
    booking_aid = st.secrets.get("BOOKING_AID","")
    aid_param = f"&aid={booking_aid}" if booking_aid else ""
    dest_enc = urllib.parse.quote(destination)
    return (
        f"https://www.booking.com/searchresults.fr.html"
        f"?ss={dest_enc}&checkin={d1}&checkout={d2}"
        f"&group_adults={adultes}&group_children={enfants}&no_rooms=1{aid_param}"
    )

@st.cache_data(ttl=300, show_spinner=False)
def get_skyscanner_prices(orig_iata, dest_iata, d1, d2, adultes):
    if not SKYSCANNER_API_KEY: return None
    url = f"https://{SKYSCANNER_HOST}/api/v1/flights/searchFlights"
    headers = {"X-RapidAPI-Key":SKYSCANNER_API_KEY,"X-RapidAPI-Host":SKYSCANNER_HOST}
    params = {"originSkyId":orig_iata,"destinationSkyId":dest_iata,"originEntityId":orig_iata,
              "destinationEntityId":dest_iata,"date":d1,"returnDate":d2,"adults":adultes,
              "currency":"EUR","locale":"fr-FR","market":"FR","countryCode":"FR","cabinClass":"economy"}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        itin = resp.json().get("data",{}).get("itineraries",{}).get("results",[])
        if itin:
            prices = [it["price"]["raw"] for it in itin if it.get("price",{}).get("raw")]
            if prices: return {"price":round(min(prices))}
    except: pass
    return None

@st.cache_data(ttl=300, show_spinner=False)
def get_booking_hotel_price(destination, d1, d2, adultes, nuits):
    if not BOOKING_API_KEY: return None
    headers = {"X-RapidAPI-Key":BOOKING_API_KEY,"X-RapidAPI-Host":BOOKING_HOST}
    try:
        r1 = requests.get(f"https://{BOOKING_HOST}/api/v1/hotels/searchDestination",
                          headers=headers, params={"query":destination}, timeout=6)
        r1.raise_for_status()
        results = r1.json().get("data",[])
        if not results: return None
        dest_id, dest_type = results[0]["dest_id"], results[0]["dest_type"]
        r2 = requests.get(f"https://{BOOKING_HOST}/api/v1/hotels/searchHotels", headers=headers,
                          params={"dest_id":dest_id,"search_type":dest_type,"arrival_date":d1,
                                  "departure_date":d2,"adults":adultes,"room_qty":1,
                                  "currency_code":"EUR","languagecode":"fr","sort_by":"popularity"}, timeout=8)
        r2.raise_for_status()
        hotels = r2.json().get("data",{}).get("hotels",[])
        if hotels:
            prices = [h["property"]["priceBreakdown"]["grossPrice"]["value"]
                      for h in hotels[:10]
                      if h.get("property",{}).get("priceBreakdown",{}).get("grossPrice",{}).get("value")]
            if prices: return {"price_per_night":round(sum(prices)/len(prices)/nuits)}
    except: pass
    return None

def build_backpacker_route(depart_ville, nb_stops, budget_total, adultes, enfants, bebes, nuits_par_etape):
    """
    Construit un circuit logique depuis le lieu de départ.
    Sélectionne les destinations les plus proches géographiquement dans la même région,
    en bouclant vers le retour.
    """
    lat0, lng0 = depart_ville["lat"], depart_ville["lng"]

    # Budget par étape (vol estimé uniquement pour filtrage)
    budget_par_etape = budget_total / (nb_stops + 1)

    candidats = []
    for d in DESTINATIONS:
        prix = prix_total(d["prix_base"], adultes, enfants, bebes)
        if prix <= budget_par_etape * 2.5:
            dist = haversine(lat0, lng0, d["lat"], d["lng"])
            candidats.append({**d, "prix_estime": prix, "dist_depart": dist})

    if len(candidats) < nb_stops:
        return []

    # Algorithme du plus proche voisin depuis le départ
    route = []
    restants = candidats.copy()
    cur_lat, cur_lng = lat0, lng0

    for _ in range(nb_stops):
        if not restants: break
        restants.sort(key=lambda x: haversine(cur_lat, cur_lng, x["lat"], x["lng"]))
        # On prend parmi les 3 plus proches celui avec le meilleur rapport qualité/prix
        pool = restants[:max(3, len(restants)//3)]
        pool.sort(key=lambda x: x["prix_estime"])
        choix = pool[0]
        route.append(choix)
        cur_lat, cur_lng = choix["lat"], choix["lng"]
        restants = [r for r in restants if r["nom"] != choix["nom"]]

    return route

# ─────────────────────────────────────────────
#  LOGO SVG
# ─────────────────────────────────────────────
LOGO_SVG = """<svg width="{w}" height="{w}" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="15" width="36" height="25" rx="4" fill="#F5F0E8" stroke="#0D0D0D" stroke-width="1.6"/>
  <path d="M4 22h36" stroke="#0D0D0D" stroke-width="1.2" stroke-linecap="square"/>
  <path d="M4 15c0-3 2.5-5.5 5.5-5.5h21c3 0 5.5 2.5 5.5 5.5" stroke="#0D0D0D" stroke-width="1.6" fill="none"/>
  <rect x="29" y="26" width="13" height="8" rx="4" fill="#0D0D0D"/>
  <circle cx="35.5" cy="30" r="1.8" fill="#F5F0E8"/>
  <g transform="translate(32,7) rotate(-35 4 3)">
    <path d="M0 3 L9 0 L9 6 Z" fill="#0D0D0D"/>
    <path d="M2 1.5 L-2 4 L0 3 Z" fill="#6B6560"/>
    <path d="M7 1 L5 5 L6.5 3 Z" fill="#6B6560"/>
  </g>
</svg>"""

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    lang_key = st.selectbox("", list(LANGS.keys()), label_visibility="collapsed")
    T = LANGS[lang_key]

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:1rem 0 0.2rem">
      {LOGO_SVG.format(w=28)}
      <span style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;font-weight:400;color:#0D0D0D;letter-spacing:0.04em">Pouch Voyage</span>
    </div>
    <hr style="margin:0.6rem 0 1.2rem">
    """, unsafe_allow_html=True)

    ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
    ville_idx = st.selectbox(T["depart"], range(len(ville_options)), format_func=lambda i: ville_options[i])
    depart_ville = VILLES_DEPART[ville_idx]
    depart_iata  = depart_ville["iata"]

    st.caption(T["dates"])
    col1, col2 = st.columns(2)
    with col1:
        d1 = st.date_input("↗", value=date.today()+timedelta(days=30), min_value=date.today(), label_visibility="collapsed")
    with col2:
        d2 = st.date_input("↙", value=date.today()+timedelta(days=60), min_value=date.today(), label_visibility="collapsed")
    st.caption(f"{d1.strftime('%d/%m/%Y')} → {d2.strftime('%d/%m/%Y')}")

    st.caption(T["budget"])
    budget = st.slider("budget", min_value=500, max_value=15000, value=5000, step=100, label_visibility="collapsed")
    st.caption(T["budget_sel"].format(b=budget))

    st.caption(T["voyageurs"])
    c1, c2, c3 = st.columns(3)
    with c1: adultes = st.number_input(T["adultes"], min_value=1, max_value=9, value=1, step=1)
    with c2: enfants = st.number_input(T["enfants"], min_value=0, max_value=9, value=0, step=1)
    with c3: bebes   = st.number_input(T["bebes"],   min_value=0, max_value=9, value=0, step=1)

    st.caption(T["nb_dest"])
    nb_stops = st.slider("nb_stops", min_value=2, max_value=8, value=4, label_visibility="collapsed")

    fav = st.text_input(T["fav"], placeholder=T["fav_ph"])
    chercher = st.button(T["search"], use_container_width=True, type="primary")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption(T["powered"])

# ─────────────────────────────────────────────
#  CONTENU PRINCIPAL
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="logo-wrap">
  {LOGO_SVG.format(w=54)}
  <div class="main-title">Pouch Voyage</div>
</div>
<div class="subtitle">{T["subtitle"]}</div>
""", unsafe_allow_html=True)

if not chercher:
    st.info(T["fill_form"])
    st.stop()

nuits_total = (d2 - d1).days
if nuits_total <= 0:
    st.error(T["date_err"])
    st.stop()

d1_str    = d1.strftime("%Y-%m-%d")
d2_str    = d2.strftime("%Y-%m-%d")
fav_lower = fav.lower().strip()
nuits_par_etape = max(1, nuits_total // (nb_stops + 1))

# ── ONGLETS ───────────────────────────────────
tab1, tab2 = st.tabs([T["tab_dest"], T["tab_back"]])

# ═══════════════════════════════════════════════
#  ONGLET 1 — DESTINATIONS
# ═══════════════════════════════════════════════
with tab1:
    resultats = []
    for dest in DESTINATIONS:
        prix_est = prix_total(dest["prix_base"], adultes, enfants, bebes)
        if prix_est > budget: continue
        score = 2 if prix_est <= budget * 0.75 else 0
        nom_lower = dest["nom"].lower() + " " + dest["pays"].lower()
        if fav_lower and (fav_lower in nom_lower or any(m in fav_lower for m in nom_lower.split())):
            score += 10
        resultats.append({
            **dest, "prix_estime":prix_est, "nuits":nuits_total,
            "reste":budget-prix_est, "score":score, "is_favorite":score>=10,
            "url_sky": build_skyscanner_url(depart_iata, dest["iata"], d1_str, d2_str, adultes, enfants, bebes),
            "url_book":build_booking_url(dest["booking_id"], d1_str, d2_str, adultes, enfants),
        })
    resultats.sort(key=lambda x: (-x["score"], x["prix_estime"]))
    resultats = resultats[:12]

    total_v = adultes + enfants + bebes
    st.markdown(f'<div class="summary-box">{T["found"].format(n=len(resultats),nuits=nuits_total,v=total_v,b=budget)}</div>', unsafe_allow_html=True)

    if not resultats:
        st.markdown(f'<div class="no-result">{T["no_result"]}</div>', unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i, r in enumerate(resultats):
            with cols[i % 2]:
                with st.container(border=True):
                    fav_txt = f" — {T['fav_label']}" if r["is_favorite"] else ""
                    st.markdown(f"{r['flag']} **{r['nom']}**{fav_txt}")
                    st.caption(r["pays"])
                    live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
                    live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits_total)
                    if live_vol:
                        st.metric(T["price_live"], f"{live_vol['price']:,} €")
                    else:
                        st.metric(T["price_est"], f"{r['prix_estime']:,} €", help=T["price_help"])
                    if live_hotel:
                        st.caption(T["hotel_live"].format(p=live_hotel["price_per_night"]))
                    st.caption("  ·  ".join(r["tags"]))
                    st.success(T["reste"].format(r=r["reste"], n=r["nuits"]))
                    c1, c2 = st.columns(2)
                    with c1: st.link_button(T["btn_sky"],  r["url_sky"],  use_container_width=True)
                    with c2: st.link_button(T["btn_book"], r["url_book"], use_container_width=True)

# ═══════════════════════════════════════════════
#  ONGLET 2 — BACKPACKER
# ═══════════════════════════════════════════════
with tab2:
    route = build_backpacker_route(depart_ville, nb_stops, budget, adultes, enfants, bebes, nuits_par_etape)

    if not route:
        st.markdown(f'<div class="no-result">{T["back_no"]}</div>', unsafe_allow_html=True)
    else:
        nuits_total_back = nuits_par_etape * nb_stops
        st.markdown(f'<div class="itin-header">{T["back_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="itin-subtitle">{T["back_sub"].format(n=nb_stops, nuits=nuits_total_back)}</div>', unsafe_allow_html=True)

        # ── Carte ────────────────────────────────
        map_col, itin_col = st.columns([1.2, 1])

        with map_col:
            # Construire les données pour la carte avec places_search
            try:
                import json
                lats = [depart_ville["lat"]] + [r["lat"] for r in route] + [depart_ville["lat"]]
                lngs = [depart_ville["lng"]] + [r["lng"] for r in route] + [depart_ville["lng"]]
                # Carte simple HTML avec Leaflet
                route_coords = [[depart_ville["lat"], depart_ville["lng"]]]
                for r in route:
                    route_coords.append([r["lat"], r["lng"]])
                route_coords.append([depart_ville["lat"], depart_ville["lng"]])

                markers_js = f"""
                  L.circleMarker([{depart_ville["lat"]},{depart_ville["lng"]}], {{
                    radius:8, color:'#0D0D0D', fillColor:'#F5F0E8', fillOpacity:1, weight:2
                  }}).addTo(map).bindPopup('<b>{depart_ville["flag"]} {depart_ville["nom"]}</b><br>Départ / Retour');
                """
                for idx, r in enumerate(route):
                    markers_js += f"""
                  L.circleMarker([{r["lat"]},{r["lng"]}], {{
                    radius:7, color:'#0D0D0D', fillColor:'#0D0D0D', fillOpacity:1, weight:2
                  }}).addTo(map).bindPopup('<b>{r["flag"]} {r["nom"]}</b><br>{r["pays"]}<br>~{r["prix_estime"]:,} €');
                    """

                coords_json = json.dumps(route_coords)
                map_html = f"""
<!DOCTYPE html><html><head>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body{{margin:0;background:#F5F0E8;}}
  #map{{height:420px;width:100%;background:#F5F0E8;}}
  .leaflet-tile{{filter:grayscale(1) contrast(0.9) brightness(1.05);}}
  .leaflet-container{{background:#EDE8DE;font-family:'Inter',sans-serif;}}
  .leaflet-popup-content-wrapper{{border-radius:0;border:1px solid #D4CFC6;box-shadow:none;}}
</style>
</head><body>
<div id="map"></div>
<script>
  var map = L.map('map', {{zoomControl:true, attributionControl:false}});
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png',{{maxZoom:18}}).addTo(map);
  var coords = {coords_json};
  L.polyline(coords, {{color:'#0D0D0D', weight:1.5, dashArray:'6,6', opacity:0.7}}).addTo(map);
  {markers_js}
  var bounds = L.latLngBounds(coords);
  map.fitBounds(bounds, {{padding:[30,30]}});
</script>
</body></html>"""
                st.components.v1.html(map_html, height=430)
            except Exception as e:
                st.caption(f"Carte non disponible : {e}")

        # ── Itinéraire ───────────────────────────
        with itin_col:
            # Budget estimé total
            cout_vol_total = sum(r["prix_estime"] for r in route)
            cout_hotel_total = sum(r["prix_base"] * 0.05 * nuits_par_etape for r in route)
            cout_total = round(cout_vol_total * 0.4 + cout_hotel_total)
            pct = min(100, round(cout_total / budget * 100))

            # Barre budget
            reste_budget = budget - cout_total
            st.markdown(f"""
<div class="budget-bar-wrap">
  <div class="budget-bar-label">{T["back_budget_used"]} · {pct}%</div>
  <div class="budget-bar-bg"><div class="budget-bar-fill" style="width:{pct}%"></div></div>
  <div class="budget-numbers">
    <span>~{cout_total:,} €</span>
    <span>{T["back_budget_rest"]} ~{max(0,reste_budget):,} €</span>
  </div>
</div>
""", unsafe_allow_html=True)

            # Étapes
            etapes = [{"nom":depart_ville["nom"],"flag":depart_ville["flag"],"pays":depart_ville["pays"],
                       "is_home":True,"tags":[]}] + \
                     [{"nom":r["nom"],"flag":r["flag"],"pays":r["pays"],"is_home":False,
                       "tags":r["tags"],"prix_estime":r["prix_estime"],
                       "iata":r["iata"],"booking_id":r["booking_id"]} for r in route] + \
                     [{"nom":depart_ville["nom"],"flag":depart_ville["flag"],"pays":depart_ville["pays"],
                       "is_home":True,"tags":[]}]

            # Date courante
            cur_date = d1

            itin_html = ""
            for idx, etape in enumerate(etapes):
                is_last = idx == len(etapes) - 1
                dot = '<div class="itin-dot-home"></div>' if etape["is_home"] else '<div class="itin-dot"></div>'
                vline = "" if is_last else '<div class="itin-vline"></div>'

                if etape["is_home"]:
                    label = T["back_retour"] if is_last else T["back_depart"]
                    meta  = cur_date.strftime("%d %b %Y")
                    prix_line = ""
                    tags_line = ""
                else:
                    label = f"{etape['flag']} {etape['nom']}"
                    meta  = f"{cur_date.strftime('%d %b')} — {(cur_date+timedelta(days=nuits_par_etape)).strftime('%d %b %Y')} · {T['back_nuits'].format(n=nuits_par_etape)}"
                    prix_line = f'<div class="itin-price">~{etape["prix_estime"]:,} €</div>'
                    tags_line = f'<div class="itin-tags">{" · ".join(etape["tags"])}</div>'
                    cur_date += timedelta(days=nuits_par_etape)

                itin_html += f"""
<div class="itin-step">
  <div class="itin-line">{dot}{vline}</div>
  <div class="itin-content">
    <div class="itin-city">{label}</div>
    <div class="itin-meta">{meta}</div>
    {prix_line}{tags_line}
  </div>
</div>"""

            st.markdown(itin_html, unsafe_allow_html=True)

        # ── Boutons par étape ─────────────────────
        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("Réservez chaque étape :")
        btn_cols = st.columns(min(len(route), 4))
        cur_date = d1
        for i, r in enumerate(route):
            d1_etape = cur_date.strftime("%Y-%m-%d")
            d2_etape = (cur_date + timedelta(days=nuits_par_etape)).strftime("%Y-%m-%d")
            prev_iata = depart_iata if i == 0 else route[i-1]["iata"]
            with btn_cols[i % len(btn_cols)]:
                st.markdown(f"**{r['flag']} {r['nom']}**")
                st.link_button(T["back_btn_sky"],
                               build_skyscanner_url(prev_iata, r["iata"], d1_etape, d2_etape, adultes, enfants, bebes),
                               use_container_width=True)
                st.link_button(T["back_btn_book"],
                               build_booking_url(r["booking_id"], d1_etape, d2_etape, adultes, enfants),
                               use_container_width=True)
            cur_date += timedelta(days=nuits_par_etape)
