"""
Pouch Voyage — Application Streamlit
Travelpayout ID: 731169
Design: photos Unsplash + cartes élégantes plein écran
"""

import streamlit as st
import requests
import urllib.parse
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
#  CONFIG PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Pouch Voyage",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  PHOTOS UNSPLASH — une par destination (libres de droits)
# ─────────────────────────────────────────────
DEST_PHOTOS = {
    "Tokyo":          "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80",
    "Rio de Janeiro": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800&q=80",
    "Chiang Mai":     "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800&q=80",
    "Malé":           "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "Cusco":          "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=800&q=80",
    "Reykjavik":      "https://images.unsplash.com/photo-1474690870753-1b92efa1f2d8?w=800&q=80",
    "Nairobi":        "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&q=80",
    "Queenstown":     "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=800&q=80",
    "Marrakech":      "https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800&q=80",
    "New York":       "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800&q=80",
    "Bali":           "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80",
    "Santorin":       "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
    "Hanoï":          "https://images.unsplash.com/photo-1555348268-f2b67b58ca3b?w=800&q=80",
    "Le Cap":         "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=800&q=80",
    "Buenos Aires":   "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=800&q=80",
    "Lisbonne":       "https://images.unsplash.com/photo-1558370781-d6196949e317?w=800&q=80",
}

# ─────────────────────────────────────────────
#  CSS — ultra élégant, fond crème, photo cover
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500&display=swap');

  :root {
    --cream:  #F5F0E8;
    --cream2: #EDE8DE;
    --ink:    #0D0D0D;
    --muted:  #6B6560;
    --border: #D4CFC6;
    --white:  #FEFCF8;
    --gold:   #C9A96E;
  }

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: var(--cream) !important;
    color: var(--ink) !important;
  }
  section[data-testid="stMain"],
  .main .block-container { background: var(--cream) !important; padding-top: 1rem !important; }
  header[data-testid="stHeader"] { background: var(--cream) !important; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
  }
  div[data-testid="stSidebarContent"] { padding: 1.6rem 1.4rem 2rem; }
  section[data-testid="stSidebar"] label {
    color: var(--ink) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  /* ── Hero titre ── */
  .hero {
    text-align: center;
    padding: 1.6rem 0 2.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.4rem;
  }
  .hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 300;
    letter-spacing: 0.08em;
    color: var(--ink);
    line-height: 1;
    margin-bottom: 0.4rem;
  }
  .hero-sub {
    font-size: 0.82rem;
    font-weight: 300;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  /* ── Summary bar ── */
  .summary {
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }
  .summary b { color: var(--ink); font-weight: 500; }
  .summary-dot { color: var(--border); }

  /* ── Carte destination ── */
  .dest-card {
    background: var(--white);
    border: 1px solid var(--border);
    margin-bottom: 1.2rem;
    overflow: hidden;
    transition: border-color 0.25s ease;
    position: relative;
  }
  .dest-card:hover { border-color: var(--ink); }

  .dest-photo {
    width: 100%;
    height: 210px;
    object-fit: cover;
    display: block;
    filter: brightness(0.93);
    transition: filter 0.4s ease, transform 0.5s ease;
  }
  .dest-card:hover .dest-photo {
    filter: brightness(1);
    transform: scale(1.02);
  }
  .photo-wrap { overflow: hidden; position: relative; }

  .dest-fav-ribbon {
    position: absolute;
    top: 14px; right: 14px;
    background: var(--ink);
    color: var(--cream);
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 4px 10px;
  }

  .dest-body { padding: 1.2rem 1.4rem 1rem; }

  .dest-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.55rem;
    font-weight: 400;
    color: var(--ink);
    line-height: 1;
    margin-bottom: 2px;
  }
  .dest-country {
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.7rem;
  }

  .dest-tags {
    display: flex; flex-wrap: wrap; gap: 5px;
    margin-bottom: 0.9rem;
  }
  .dest-tag {
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 2px 9px;
  }

  .dest-price-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1px solid var(--border);
    padding-top: 0.9rem;
    margin-bottom: 0.9rem;
  }
  .dest-price {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 400;
    color: var(--ink);
    line-height: 1;
  }
  .dest-price-label {
    font-size: 0.68rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 2px;
  }
  .dest-nights {
    font-size: 0.72rem;
    color: var(--muted);
    text-align: right;
    letter-spacing: 0.05em;
  }
  .dest-reste {
    font-size: 0.72rem;
    color: var(--gold);
    letter-spacing: 0.05em;
    margin-top: 2px;
  }

  .dest-hotel {
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin-bottom: 0.9rem;
    font-style: italic;
  }

  /* ── Boutons affiliés ── */
  .btn-row {
    display: flex;
    gap: 8px;
  }
  .btn-aff {
    flex: 1;
    display: block;
    text-align: center;
    padding: 9px 0;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-decoration: none !important;
    border: 1px solid var(--ink);
    color: var(--ink) !important;
    background: transparent;
    transition: background 0.2s, color 0.2s;
    font-family: 'Inter', sans-serif;
  }
  .btn-aff:hover { background: var(--ink); color: var(--cream) !important; }
  .btn-aff-dark {
    background: var(--ink);
    color: var(--cream) !important;
  }
  .btn-aff-dark:hover { background: var(--cream2); color: var(--ink) !important; border-color: var(--ink); }

  /* bouton sidebar */
  div[data-testid="stButton"] button {
    background: var(--ink) !important; color: var(--cream) !important;
    border: 1px solid var(--ink) !important; border-radius: 0 !important;
    font-size: 0.75rem !important; letter-spacing: 0.1em; text-transform: uppercase;
    font-weight: 400 !important;
  }
  div[data-testid="stButton"] button:hover {
    background: var(--cream2) !important; color: var(--ink) !important;
  }

  /* ── Link buttons — raffinés, minimalistes ── */
  div[data-testid="stLinkButton"] a {
    background: transparent !important;
    color: var(--muted) !important;
    border: none !important;
    border-bottom: 1px solid var(--border) !important;
    border-radius: 0 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    font-style: italic !important;
    letter-spacing: 0.04em !important;
    text-transform: none !important;
    padding: 4px 0 !important;
    width: 100% !important;
    display: block !important;
    text-align: center !important;
    transition: color 0.2s ease, border-color 0.2s ease !important;
  }
  div[data-testid="stLinkButton"] a:hover {
    color: var(--ink) !important;
    border-bottom-color: var(--ink) !important;
    background: transparent !important;
  }

  /* slider */
  div[data-testid="stSlider"] > div > div > div { background: var(--ink) !important; }

  /* no result */
  .no-result { text-align:center; padding:5rem 2rem; color:var(--muted); font-size:0.9rem; font-weight:300; letter-spacing:0.05em; }

  /* info / error */
  div[data-testid="stAlert"] {
    background: var(--cream2) !important; border: 1px solid var(--border) !important;
    border-radius: 0 !important; color: var(--muted) !important; font-size: 0.82rem !important;
  }

  /* caption */
  .stCaption, [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }

  /* grid espace */
  .grid-gap { margin-top: 0.4rem; }

  /* divider */
  hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

  .powered {
    font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--border); margin-top: 1.5rem; text-align: center;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONFIGURATION
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
        "subtitle":   "Voyagez selon votre budget",
        "depart":     "Départ",
        "dates":      "Dates",
        "budget":     "Budget total",
        "budget_cap": "{b:,} €",
        "voyageurs":  "Voyageurs",
        "adultes":    "Adultes",
        "enfants":    "Enfants",
        "bebes":      "Bébés",
        "fav":        "Destination (optionnel)",
        "fav_ph":     "Tokyo, Bali…",
        "search":     "Rechercher",
        "powered":    "Propulsé par Travelpayout",
        "tab_search":  "✈  Recherche",
        "tab_cost":    "◻  Coût de la vie",
        "cost_title":  "Coût de la vie par jour",
        "cost_sub":    "Entrez une ville pour estimer votre budget quotidien",
        "cost_input":  "Ville de destination",
        "cost_ph":     "ex : Bangkok, Lisbonne, New York…",
        "cost_btn":    "Calculer",
        "cost_ndays":  "Nombre de jours",
        "cost_total":  "Budget total estimé",
        "cost_src":    "Source : Numbeo (données moyennes)",
        "cost_err":    "Ville introuvable. Essayez un autre nom.",
        "cost_cats": {
            "repas":    "Repas",
            "transport":"Transport",
            "logement": "Logement",
            "loisirs":  "Loisirs & divers",
        },
        "fill_form":  "Remplissez le formulaire et lancez la recherche.",
        "date_err":   "La date de retour doit être après la date de départ.",
        "found":      "{n} destination(s) · {nuits} nuit(s) · {v} voyageur(s) · {b:,} €",
        "no_result":  "Aucune destination dans ce budget.",
        "price_live": "Vol dès",
        "price_est":  "Estimé dès",
        "price_help": "Prix indicatif — confirmez sur Skyscanner.",
        "hotel_live": "Hôtel : ~{p:,} €/nuit",
        "reste":      "+{r:,} € restant · {n} nuits",
        "btn_sky":    "✈  Skyscanner",
        "btn_book":   "◻  Booking",
        "fav_label":  "Favori",
        "per_pax":    "pour {v} voyageur(s)",
    },
    "🇬🇧 English": {
        "subtitle":   "Travel within your budget",
        "depart":     "Departure",
        "dates":      "Dates",
        "budget":     "Total budget",
        "budget_cap": "€{b:,}",
        "voyageurs":  "Travellers",
        "adultes":    "Adults",
        "enfants":    "Children",
        "bebes":      "Infants",
        "fav":        "Destination (optional)",
        "fav_ph":     "Tokyo, Bali…",
        "search":     "Search",
        "powered":    "Powered by Travelpayout",
        "tab_search":  "✈  Search",
        "tab_cost":    "◻  Cost of living",
        "cost_title":  "Daily cost of living",
        "cost_sub":    "Enter a city to estimate your daily budget",
        "cost_input":  "Destination city",
        "cost_ph":     "e.g. Bangkok, Lisbon, New York…",
        "cost_btn":    "Calculate",
        "cost_ndays":  "Number of days",
        "cost_total":  "Estimated total budget",
        "cost_src":    "Source: Numbeo (average data)",
        "cost_err":    "City not found. Try another name.",
        "cost_cats": {
            "repas":    "Meals",
            "transport":"Transport",
            "logement": "Accommodation",
            "loisirs":  "Leisure & misc",
        },
        "fill_form":  "Fill the form and click Search.",
        "date_err":   "Return date must be after departure.",
        "found":      "{n} destination(s) · {nuits} night(s) · {v} traveller(s) · €{b:,}",
        "no_result":  "No destinations in this budget.",
        "price_live": "Flight from",
        "price_est":  "Estimated from",
        "price_help": "Indicative — confirm on Skyscanner.",
        "hotel_live": "Hotel: ~€{p:,}/night",
        "reste":      "+€{r:,} remaining · {n} nights",
        "btn_sky":    "✈  Skyscanner",
        "btn_book":   "◻  Booking",
        "fav_label":  "Favourite",
        "per_pax":    "for {v} traveller(s)",
    },
    "🇪🇸 Español": {
        "subtitle":   "Viaja según tu presupuesto",
        "depart":     "Salida",
        "dates":      "Fechas",
        "budget":     "Presupuesto total",
        "budget_cap": "{b:,} €",
        "voyageurs":  "Viajeros",
        "adultes":    "Adultos",
        "enfants":    "Niños",
        "bebes":      "Bebés",
        "fav":        "Destino (opcional)",
        "fav_ph":     "Tokio, Bali…",
        "search":     "Buscar",
        "powered":    "Desarrollado por Travelpayout",
        "tab_search":  "✈  Búsqueda",
        "tab_cost":    "◻  Coste de vida",
        "cost_title":  "Coste de vida por día",
        "cost_sub":    "Introduce una ciudad para estimar tu presupuesto diario",
        "cost_input":  "Ciudad de destino",
        "cost_ph":     "ej: Bangkok, Lisboa, Nueva York…",
        "cost_btn":    "Calcular",
        "cost_ndays":  "Número de días",
        "cost_total":  "Presupuesto total estimado",
        "cost_src":    "Fuente: Numbeo (datos medios)",
        "cost_err":    "Ciudad no encontrada. Prueba otro nombre.",
        "cost_cats": {
            "repas":    "Comidas",
            "transport":"Transporte",
            "logement": "Alojamiento",
            "loisirs":  "Ocio y varios",
        },
        "fill_form":  "Rellena el formulario y haz clic en Buscar.",
        "date_err":   "La fecha de regreso debe ser posterior.",
        "found":      "{n} destino(s) · {nuits} noche(s) · {v} viajero(s) · {b:,} €",
        "no_result":  "Ningún destino en este presupuesto.",
        "price_live": "Vuelo desde",
        "price_est":  "Estimado desde",
        "price_help": "Indicativo — confirma en Skyscanner.",
        "hotel_live": "Hotel: ~{p:,} €/noche",
        "reste":      "+{r:,} € restante · {n} noches",
        "btn_sky":    "✈  Skyscanner",
        "btn_book":   "◻  Booking",
        "fav_label":  "Favorito",
        "per_pax":    "para {v} viajero(s)",
    },
}

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
    {"flag":"🇯🇵","nom":"Tokyo",          "pays":"Japon",          "iata":"TYO","booking_id":"Tokyo",         "tags":["Culture","Gastronomie","Modernité"],  "prix_base":2200},
    {"flag":"🇧🇷","nom":"Rio de Janeiro", "pays":"Brésil",         "iata":"GIG","booking_id":"Rio de Janeiro","tags":["Plage","Fête","Nature"],              "prix_base":1800},
    {"flag":"🇹🇭","nom":"Chiang Mai",     "pays":"Thaïlande",      "iata":"CNX","booking_id":"Chiang Mai",    "tags":["Temples","Nature","Détente"],         "prix_base":950},
    {"flag":"🇲🇻","nom":"Malé",           "pays":"Maldives",       "iata":"MLE","booking_id":"Male",          "tags":["Luxe","Plage","Snorkeling"],          "prix_base":4500},
    {"flag":"🇵🇪","nom":"Cusco",          "pays":"Pérou",          "iata":"LIM","booking_id":"Cusco",         "tags":["Aventure","Histoire","Randonnée"],    "prix_base":2600},
    {"flag":"🇮🇸","nom":"Reykjavik",      "pays":"Islande",        "iata":"KEF","booking_id":"Reykjavik",     "tags":["Aurores","Nature","Volcans"],         "prix_base":2100},
    {"flag":"🇰🇪","nom":"Nairobi",        "pays":"Kenya",          "iata":"NBO","booking_id":"Nairobi",       "tags":["Safari","Faune","Savane"],            "prix_base":3200},
    {"flag":"🇳🇿","nom":"Queenstown",     "pays":"Nv-Zélande",     "iata":"ZQN","booking_id":"Queenstown",    "tags":["Aventure","Paysages","Sport"],        "prix_base":5200},
    {"flag":"🇲🇦","nom":"Marrakech",      "pays":"Maroc",          "iata":"RAK","booking_id":"Marrakech",     "tags":["Souk","Culture","Désert"],            "prix_base":800},
    {"flag":"🇺🇸","nom":"New York",       "pays":"États-Unis",     "iata":"JFK","booking_id":"New York City", "tags":["Ville","Shopping","Culture"],         "prix_base":2900},
    {"flag":"🇮🇩","nom":"Bali",           "pays":"Indonésie",      "iata":"DPS","booking_id":"Bali",          "tags":["Spiritualité","Plage","Jungle"],      "prix_base":1400},
    {"flag":"🇬🇷","nom":"Santorin",       "pays":"Grèce",          "iata":"JTR","booking_id":"Santorini",     "tags":["Romance","Mer","Gastronomie"],        "prix_base":1600},
    {"flag":"🇻🇳","nom":"Hanoï",          "pays":"Vietnam",        "iata":"HAN","booking_id":"Hanoi",         "tags":["Rue","Histoire","Gastronomie"],       "prix_base":1100},
    {"flag":"🇿🇦","nom":"Le Cap",         "pays":"Afrique du Sud", "iata":"CPT","booking_id":"Cape Town",     "tags":["Nature","Vignobles","Mer"],           "prix_base":2400},
    {"flag":"🇦🇷","nom":"Buenos Aires",   "pays":"Argentine",      "iata":"EZE","booking_id":"Buenos Aires",  "tags":["Tango","Gastronomie","Culture"],      "prix_base":2000},
    {"flag":"🇵🇹","nom":"Lisbonne",       "pays":"Portugal",       "iata":"LIS","booking_id":"Lisbon",        "tags":["Histoire","Fado","Gastronomie"],      "prix_base":700},
]

# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────
def prix_total(prix_base, adultes, enfants, bebes):
    return round(prix_base * adultes + prix_base * 0.70 * enfants + prix_base * 0.10 * bebes)

def build_skyscanner_url(orig, dest, d1, d2, adultes, enfants, bebes):
    fmt = lambda d: d.replace("-", "")
    return (
        f"https://www.skyscanner.fr/transport/vols/"
        f"{orig.lower()}/{dest.lower()}/{fmt(d1)}/{fmt(d2)}/"
        f"?adults={adultes}&children={enfants}&infants={bebes}"
        f"&utm_source=travelpayout&utm_medium=affiliate&utm_campaign={TRAVELPAYOUT_ID}"
    )

def build_booking_url(destination, d1, d2, adultes, enfants):
    booking_aid = st.secrets.get("BOOKING_AID", "")
    aid_param = f"&aid={booking_aid}" if booking_aid else ""
    dest_enc = urllib.parse.quote(destination)
    return (
        f"https://www.booking.com/searchresults.fr.html"
        f"?ss={dest_enc}&checkin={d1}&checkout={d2}"
        f"&group_adults={adultes}&group_children={enfants}&no_rooms=1"
        f"{aid_param}"
    )

@st.cache_data(ttl=300, show_spinner=False)
def get_skyscanner_prices(orig_iata, dest_iata, d1, d2, adultes):
    if not SKYSCANNER_API_KEY:
        return None
    url = f"https://{SKYSCANNER_HOST}/api/v1/flights/searchFlights"
    headers = {"X-RapidAPI-Key": SKYSCANNER_API_KEY, "X-RapidAPI-Host": SKYSCANNER_HOST}
    params = {
        "originSkyId": orig_iata, "destinationSkyId": dest_iata,
        "originEntityId": orig_iata, "destinationEntityId": dest_iata,
        "date": d1, "returnDate": d2, "adults": adultes,
        "currency": "EUR", "locale": "fr-FR", "market": "FR",
        "countryCode": "FR", "cabinClass": "economy",
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        itineraries = data.get("data", {}).get("itineraries", {}).get("results", [])
        if itineraries:
            prices = [it["price"]["raw"] for it in itineraries if it.get("price", {}).get("raw")]
            if prices:
                return {"price": round(min(prices)), "currency": "EUR"}
    except Exception:
        pass
    return None

@st.cache_data(ttl=300, show_spinner=False)
def get_booking_hotel_price(destination, d1, d2, adultes, nuits):
    if not BOOKING_API_KEY:
        return None
    headers = {"X-RapidAPI-Key": BOOKING_API_KEY, "X-RapidAPI-Host": BOOKING_HOST}
    try:
        r1 = requests.get(
            f"https://{BOOKING_HOST}/api/v1/hotels/searchDestination",
            headers=headers, params={"query": destination}, timeout=6
        )
        r1.raise_for_status()
        results = r1.json().get("data", [])
        if not results:
            return None
        dest_id, dest_type = results[0]["dest_id"], results[0]["dest_type"]
        r2 = requests.get(
            f"https://{BOOKING_HOST}/api/v1/hotels/searchHotels",
            headers=headers,
            params={
                "dest_id": dest_id, "search_type": dest_type,
                "arrival_date": d1, "departure_date": d2,
                "adults": adultes, "room_qty": 1,
                "currency_code": "EUR", "languagecode": "fr", "sort_by": "popularity",
            },
            timeout=8
        )
        r2.raise_for_status()
        hotels = r2.json().get("data", {}).get("hotels", [])
        if hotels:
            prices = [
                h["property"]["priceBreakdown"]["grossPrice"]["value"]
                for h in hotels[:10]
                if h.get("property", {}).get("priceBreakdown", {}).get("grossPrice", {}).get("value")
            ]
            if prices:
                return {"price_per_night": round(sum(prices) / len(prices) / nuits)}
    except Exception:
        pass
    return None

def render_card(r, T, depart_iata, d1_str, d2_str, adultes, nuits, total_v):
    """Retourne (html_sans_boutons, live_vol, live_hotel) — les boutons sont rendus via st.link_button."""
    photo_url = DEST_PHOTOS.get(r["nom"], "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80")
    fav_ribbon = f'<div class="dest-fav-ribbon">★ {T["fav_label"]}</div>' if r["is_favorite"] else ""
    tags_html  = "".join(f'<span class="dest-tag">{t}</span>' for t in r["tags"])

    live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
    live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits)

    if live_vol:
        price_label = T["price_live"]
        price_val   = f"{live_vol['price']:,} €"
    else:
        price_label = T["price_est"]
        price_val   = f"{r['prix_estime']:,} €"

    hotel_line = f'<div class="dest-hotel">{T["hotel_live"].format(p=live_hotel["price_per_night"])}</div>' if live_hotel else ""
    per_pax    = T["per_pax"].format(v=total_v)
    reste_txt  = T["reste"].format(r=r["reste"], n=r["nuits"])

    html = f"""
<div class="dest-card">
  <div class="photo-wrap">
    <img class="dest-photo" src="{photo_url}" alt="{r['nom']}" loading="lazy">
    {fav_ribbon}
  </div>
  <div class="dest-body">
    <div class="dest-name">{r['flag']} {r['nom']}</div>
    <div class="dest-country">{r['pays']}</div>
    <div class="dest-tags">{tags_html}</div>
    <div class="dest-price-row">
      <div>
        <div style="font-size:0.68rem;letter-spacing:0.07em;text-transform:uppercase;color:var(--muted);margin-bottom:2px">{price_label}</div>
        <div class="dest-price">{price_val}</div>
        <div class="dest-price-label">{per_pax}</div>
      </div>
      <div>
        <div class="dest-nights">{r['nuits']} nuits</div>
        <div class="dest-reste">{reste_txt}</div>
      </div>
    </div>
    {hotel_line}
  </div>
</div>
"""
    return html

# ─────────────────────────────────────────────
#  COÛT DE LA VIE — données Numbeo via leur API publique
# ─────────────────────────────────────────────
# Base de données locale enrichie (€/jour/personne) pour les villes populaires
COST_DB = {
    # Asie
    "bangkok":       {"repas": 12, "transport": 4,  "logement": 25, "loisirs": 10},
    "chiang mai":    {"repas": 10, "transport": 3,  "logement": 20, "loisirs": 8},
    "bali":          {"repas": 14, "transport": 5,  "logement": 35, "loisirs": 12},
    "tokyo":         {"repas": 28, "transport": 10, "logement": 80, "loisirs": 20},
    "kyoto":         {"repas": 25, "transport": 8,  "logement": 70, "loisirs": 18},
    "osaka":         {"repas": 22, "transport": 8,  "logement": 65, "loisirs": 16},
    "séoul":         {"repas": 18, "transport": 5,  "logement": 55, "loisirs": 15},
    "seoul":         {"repas": 18, "transport": 5,  "logement": 55, "loisirs": 15},
    "hanoi":         {"repas": 8,  "transport": 3,  "logement": 20, "loisirs": 7},
    "hanoï":         {"repas": 8,  "transport": 3,  "logement": 20, "loisirs": 7},
    "ho chi minh":   {"repas": 9,  "transport": 3,  "logement": 22, "loisirs": 8},
    "singapour":     {"repas": 22, "transport": 8,  "logement": 90, "loisirs": 20},
    "singapore":     {"repas": 22, "transport": 8,  "logement": 90, "loisirs": 20},
    "kuala lumpur":  {"repas": 12, "transport": 4,  "logement": 30, "loisirs": 10},
    "male":          {"repas": 30, "transport": 15, "logement": 150,"loisirs": 25},
    "malé":          {"repas": 30, "transport": 15, "logement": 150,"loisirs": 25},
    "kathmandu":     {"repas": 8,  "transport": 2,  "logement": 15, "loisirs": 6},
    "phuket":        {"repas": 15, "transport": 6,  "logement": 40, "loisirs": 12},
    "ubud":          {"repas": 12, "transport": 5,  "logement": 30, "loisirs": 10},
    # Europe
    "paris":         {"repas": 35, "transport": 10, "logement": 100,"loisirs": 25},
    "lisbonne":      {"repas": 22, "transport": 6,  "logement": 60, "loisirs": 18},
    "lisbon":        {"repas": 22, "transport": 6,  "logement": 60, "loisirs": 18},
    "barcelone":     {"repas": 28, "transport": 8,  "logement": 75, "loisirs": 20},
    "barcelona":     {"repas": 28, "transport": 8,  "logement": 75, "loisirs": 20},
    "madrid":        {"repas": 26, "transport": 7,  "logement": 70, "loisirs": 18},
    "rome":          {"repas": 30, "transport": 8,  "logement": 80, "loisirs": 20},
    "amsterdam":     {"repas": 32, "transport": 9,  "logement": 90, "loisirs": 22},
    "berlin":        {"repas": 25, "transport": 7,  "logement": 65, "loisirs": 18},
    "prague":        {"repas": 18, "transport": 5,  "logement": 45, "loisirs": 14},
    "budapest":      {"repas": 16, "transport": 4,  "logement": 40, "loisirs": 12},
    "athènes":       {"repas": 22, "transport": 5,  "logement": 55, "loisirs": 15},
    "athens":        {"repas": 22, "transport": 5,  "logement": 55, "loisirs": 15},
    "santorin":      {"repas": 35, "transport": 8,  "logement": 120,"loisirs": 25},
    "santorini":     {"repas": 35, "transport": 8,  "logement": 120,"loisirs": 25},
    "reykjavik":     {"repas": 50, "transport": 15, "logement": 120,"loisirs": 30},
    "stockholm":     {"repas": 40, "transport": 12, "logement": 100,"loisirs": 25},
    "copenhague":    {"repas": 45, "transport": 12, "logement": 110,"loisirs": 28},
    "copenhagen":    {"repas": 45, "transport": 12, "logement": 110,"loisirs": 28},
    "vienne":        {"repas": 30, "transport": 9,  "logement": 80, "loisirs": 20},
    "vienna":        {"repas": 30, "transport": 9,  "logement": 80, "loisirs": 20},
    "bruxelles":     {"repas": 28, "transport": 8,  "logement": 80, "loisirs": 20},
    "brussels":      {"repas": 28, "transport": 8,  "logement": 80, "loisirs": 20},
    "genève":        {"repas": 55, "transport": 15, "logement": 130,"loisirs": 35},
    "geneva":        {"repas": 55, "transport": 15, "logement": 130,"loisirs": 35},
    "zurich":        {"repas": 60, "transport": 16, "logement": 140,"loisirs": 38},
    "marrakech":     {"repas": 14, "transport": 4,  "logement": 35, "loisirs": 10},
    "dubrovnik":     {"repas": 30, "transport": 7,  "logement": 85, "loisirs": 20},
    # Amériques
    "new york":      {"repas": 45, "transport": 12, "logement": 150,"loisirs": 30},
    "new york city": {"repas": 45, "transport": 12, "logement": 150,"loisirs": 30},
    "los angeles":   {"repas": 40, "transport": 15, "logement": 130,"loisirs": 28},
    "miami":         {"repas": 38, "transport": 14, "logement": 120,"loisirs": 26},
    "san francisco": {"repas": 50, "transport": 14, "logement": 160,"loisirs": 32},
    "chicago":       {"repas": 38, "transport": 10, "logement": 110,"loisirs": 25},
    "montréal":      {"repas": 30, "transport": 8,  "logement": 80, "loisirs": 20},
    "montreal":      {"repas": 30, "transport": 8,  "logement": 80, "loisirs": 20},
    "toronto":       {"repas": 32, "transport": 9,  "logement": 90, "loisirs": 22},
    "vancouver":     {"repas": 35, "transport": 10, "logement": 100,"loisirs": 24},
    "mexico":        {"repas": 15, "transport": 5,  "logement": 35, "loisirs": 10},
    "cancun":        {"repas": 20, "transport": 7,  "logement": 60, "loisirs": 15},
    "buenos aires":  {"repas": 12, "transport": 3,  "logement": 30, "loisirs": 8},
    "rio de janeiro":{"repas": 18, "transport": 5,  "logement": 50, "loisirs": 12},
    "cusco":         {"repas": 12, "transport": 4,  "logement": 28, "loisirs": 9},
    "medellin":      {"repas": 12, "transport": 3,  "logement": 28, "loisirs": 8},
    "bogota":        {"repas": 13, "transport": 3,  "logement": 30, "loisirs": 9},
    # Afrique & Moyen-Orient
    "nairobi":       {"repas": 16, "transport": 5,  "logement": 40, "loisirs": 10},
    "le cap":        {"repas": 18, "transport": 6,  "logement": 45, "loisirs": 12},
    "cape town":     {"repas": 18, "transport": 6,  "logement": 45, "loisirs": 12},
    "dubaï":         {"repas": 35, "transport": 12, "logement": 110,"loisirs": 28},
    "dubai":         {"repas": 35, "transport": 12, "logement": 110,"loisirs": 28},
    "istanbul":      {"repas": 16, "transport": 4,  "logement": 40, "loisirs": 12},
    # Océanie
    "sydney":        {"repas": 40, "transport": 10, "logement": 110,"loisirs": 28},
    "melbourne":     {"repas": 38, "transport": 9,  "logement": 100,"loisirs": 26},
    "queenstown":    {"repas": 35, "transport": 10, "logement": 90, "loisirs": 22},
    "auckland":      {"repas": 38, "transport": 10, "logement": 95, "loisirs": 24},
}

def get_cost_of_living(city: str) -> dict | None:
    """Cherche la ville dans la base locale, puis tente Numbeo si absent."""
    key = city.lower().strip()
    if key in COST_DB:
        return COST_DB[key]
    # Tentative Numbeo API publique (sans clé)
    try:
        url = f"https://www.numbeo.com/api/city_prices?api_key=free&query={urllib.parse.quote(city)}&currency=EUR"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            items = {item["item_id"]: item["average_price"] for item in data.get("prices", [])}
            if items:
                repas    = round((items.get(1, 0) + items.get(2, 0)) / 2)   # restaurant
                transport= round(items.get(20, 0) * 2)                       # ticket x2
                logement = round(items.get(26, 0) / 30)                      # loyer /30
                loisirs  = round(items.get(44, 0) + items.get(28, 0))        # cinema + fitness
                if repas > 0:
                    return {"repas": repas, "transport": transport or 5,
                            "logement": logement or 40, "loisirs": loisirs or 12}
    except Exception:
        pass
    return None

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    lang_key = st.selectbox("", list(LANGS.keys()), label_visibility="collapsed")
    T = LANGS[lang_key]

    st.markdown("""
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:300;
                letter-spacing:0.08em;color:#0D0D0D;margin:0.8rem 0 0.2rem">
      ✈ Pouch Voyage
    </div>
    <hr>
    """, unsafe_allow_html=True)

    ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
    ville_idx = st.selectbox(T["depart"], range(len(ville_options)),
                             format_func=lambda i: ville_options[i])
    depart_iata = VILLES_DEPART[ville_idx]["iata"]

    st.caption(T["dates"])
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        d1 = st.date_input("↗", value=date.today() + timedelta(days=30),
                           min_value=date.today(), label_visibility="collapsed")
    with col_d2:
        d2 = st.date_input("↙", value=date.today() + timedelta(days=37),
                           min_value=date.today(), label_visibility="collapsed")
    st.caption(f"{d1.strftime('%d/%m/%Y')} → {d2.strftime('%d/%m/%Y')}")

    st.markdown(f"<div style='font-size:0.78rem;letter-spacing:0.06em;text-transform:uppercase;color:#6B6560;margin-top:0.8rem;margin-bottom:4px'>{T['budget']}</div>", unsafe_allow_html=True)
    budget = st.slider("budget_slider", min_value=500, max_value=10000,
                       value=3000, step=100, label_visibility="collapsed")
    st.caption(T["budget_cap"].format(b=budget))

    st.markdown(f"<div style='font-size:0.78rem;letter-spacing:0.06em;text-transform:uppercase;color:#6B6560;margin-top:0.8rem;margin-bottom:4px'>{T['voyageurs']}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        adultes = st.number_input(T["adultes"], min_value=1, max_value=9, value=2, step=1)
    with c2:
        enfants = st.number_input(T["enfants"], min_value=0, max_value=9, value=0, step=1)
    with c3:
        bebes = st.number_input(T["bebes"], min_value=0, max_value=9, value=0, step=1)

    fav = st.text_input(T["fav"], placeholder=T["fav_ph"])
    chercher = st.button(T["search"], use_container_width=True, type="primary")

    st.markdown(f'<div class="powered">{T["powered"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONTENU PRINCIPAL
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-title">Pouch Voyage</div>
  <div class="hero-sub">{T["subtitle"]}</div>
</div>
""", unsafe_allow_html=True)

tab_search, tab_cost = st.tabs([T["tab_search"], T["tab_cost"]])

# ══════════════════════════════════════════════
#  ONGLET 1 — RECHERCHE DE VOYAGES
# ══════════════════════════════════════════════
with tab_search:
    if not chercher:
        st.markdown(f'<div class="no-result">{T["fill_form"]}</div>', unsafe_allow_html=True)
        st.stop()

    nuits = (d2 - d1).days
    if nuits <= 0:
        st.error(T["date_err"])
        st.stop()

    d1_str    = d1.strftime("%Y-%m-%d")
    d2_str    = d2.strftime("%Y-%m-%d")
    fav_lower = fav.lower().strip()
    total_v   = adultes + enfants + bebes

    resultats = []
    for dest in DESTINATIONS:
        prix_est = prix_total(dest["prix_base"], adultes, enfants, bebes)
        if prix_est > budget:
            continue
        score = 2 if prix_est <= budget * 0.75 else 0
        nom_lower = dest["nom"].lower() + " " + dest["pays"].lower()
        if fav_lower and (fav_lower in nom_lower or any(m in fav_lower for m in nom_lower.split())):
            score += 10
        resultats.append({
            **dest,
            "prix_estime": prix_est,
            "nuits":       nuits,
            "reste":       budget - prix_est,
            "score":       score,
            "is_favorite": score >= 10,
            "url_sky":     build_skyscanner_url(depart_iata, dest["iata"], d1_str, d2_str, adultes, enfants, bebes),
            "url_book":    build_booking_url(dest["booking_id"], d1_str, d2_str, adultes, enfants),
        })

    resultats.sort(key=lambda x: (-x["score"], x["prix_estime"]))
    resultats = resultats[:12]

    st.markdown(f"""
<div class="summary">
  <b>{len(resultats)}</b> destination(s)
  <span class="summary-dot">·</span>
  <b>{nuits}</b> nuit(s)
  <span class="summary-dot">·</span>
  <b>{total_v}</b> voyageur(s)
  <span class="summary-dot">·</span>
  <b>{budget:,} €</b>
</div>
""", unsafe_allow_html=True)

    if not resultats:
        st.markdown(f'<div class="no-result">{T["no_result"]}</div>', unsafe_allow_html=True)
    else:
        cols = st.columns(3)
        for i, r in enumerate(resultats):
            with cols[i % 3]:
                html = render_card(r, T, depart_iata, d1_str, d2_str, adultes, nuits, total_v)
                st.markdown(html, unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                with b1:
                    st.link_button(T["btn_sky"], r["url_sky"], use_container_width=True)
                with b2:
                    st.link_button(T["btn_book"], r["url_book"], use_container_width=True)
                st.markdown("<div style='margin-bottom:1.2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ONGLET 2 — COÛT DE LA VIE
# ══════════════════════════════════════════════
with tab_cost:
    st.markdown(f"""
<div class="hero" style="padding:1.2rem 0 1.8rem; margin-bottom:1.5rem;">
  <div class="hero-title" style="font-size:2.2rem;">{T["cost_title"]}</div>
  <div class="hero-sub">{T["cost_sub"]}</div>
</div>
""", unsafe_allow_html=True)

    col_inp, col_days, col_btn = st.columns([3, 1, 1])
    with col_inp:
        city_input = st.text_input(T["cost_input"], placeholder=T["cost_ph"],
                                   label_visibility="collapsed")
    with col_days:
        nb_days = st.number_input(T["cost_ndays"], min_value=1, max_value=365,
                                  value=7, step=1, label_visibility="collapsed")
    with col_btn:
        calc_btn = st.button(T["cost_btn"], use_container_width=True)

    if calc_btn and city_input.strip():
        cost = get_cost_of_living(city_input.strip())
        if not cost:
            st.error(T["cost_err"])
        else:
            cats   = T["cost_cats"]
            total  = sum(cost.values())
            icons  = {"repas": "🍽", "transport": "🚌", "logement": "🏨", "loisirs": "🎭"}
            colors = {"repas": "#C9A96E", "transport": "#8BA888", "logement": "#7B9CB8", "loisirs": "#B8847B"}

            # Carte résumé principale
            st.markdown(f"""
<div class="dest-card" style="max-width:520px;margin:0 auto 2rem;">
  <div class="dest-body">
    <div class="dest-name" style="font-size:2rem;">{city_input.strip().title()}</div>
    <div class="dest-country" style="margin-bottom:1.2rem;">{T["cost_src"]}</div>
    <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:1.4rem;">
""", unsafe_allow_html=True)

            for key, label in cats.items():
                val  = cost[key]
                pct  = round(val / total * 100)
                col  = colors[key]
                icon = icons[key]
                st.markdown(f"""
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:28px;text-align:center;font-size:1rem;">{icon}</div>
        <div style="flex:1;">
          <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
            <span style="font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted)">{label}</span>
            <span style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:var(--ink)">{val} €</span>
          </div>
          <div style="height:3px;background:var(--border);border-radius:0;">
            <div style="height:3px;width:{pct}%;background:{col};transition:width 0.4s ease;"></div>
          </div>
        </div>
      </div>
""", unsafe_allow_html=True)

            st.markdown(f"""
    </div>
    <div class="dest-price-row" style="margin-bottom:0;">
      <div>
        <div style="font-size:0.68rem;letter-spacing:0.07em;text-transform:uppercase;color:var(--muted);margin-bottom:2px">Par jour</div>
        <div class="dest-price">{total} €</div>
      </div>
      <div style="text-align:right;">
        <div class="dest-nights">{nb_days} jour(s)</div>
        <div class="dest-reste" style="font-size:1rem;font-family:'Cormorant Garamond',serif;">≈ {total * nb_days:,} €</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    elif calc_btn:
        st.warning("Entrez le nom d'une ville.")
    else:
        st.markdown('<div class="no-result">Tapez une ville ci-dessus et cliquez sur Calculer.</div>', unsafe_allow_html=True)
