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
        "fill_form":  "Remplissez le formulaire et lancez la recherche.",
        "date_err":   "La date de retour doit être après la date de départ.",
        "found":      "{n} destination(s) · {nuits} nuit(s) · {v} voyageur(s) · {b:,} €",
        "no_result":  "Aucune destination dans ce budget.",
        "price_live": "Vol dès",
        "price_est":  "Estimé dès",
        "price_help": "Prix indicatif — confirmez sur Skyscanner.",
        "hotel_live": "Hôtel : ~{p:,} €/nuit",
        "reste":      "+{r:,} € restant · {n} nuits",
        "btn_sky":    "Vol — Skyscanner",
        "btn_book":   "Hôtel — Booking",
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
        "fill_form":  "Fill the form and click Search.",
        "date_err":   "Return date must be after departure.",
        "found":      "{n} destination(s) · {nuits} night(s) · {v} traveller(s) · €{b:,}",
        "no_result":  "No destinations in this budget.",
        "price_live": "Flight from",
        "price_est":  "Estimated from",
        "price_help": "Indicative — confirm on Skyscanner.",
        "hotel_live": "Hotel: ~€{p:,}/night",
        "reste":      "+€{r:,} remaining · {n} nights",
        "btn_sky":    "Flight — Skyscanner",
        "btn_book":   "Hotel — Booking",
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
        "fill_form":  "Rellena el formulario y haz clic en Buscar.",
        "date_err":   "La fecha de regreso debe ser posterior.",
        "found":      "{n} destino(s) · {nuits} noche(s) · {v} viajero(s) · {b:,} €",
        "no_result":  "Ningún destino en este presupuesto.",
        "price_live": "Vuelo desde",
        "price_est":  "Estimado desde",
        "price_help": "Indicativo — confirma en Skyscanner.",
        "hotel_live": "Hotel: ~{p:,} €/noche",
        "reste":      "+{r:,} € restante · {n} noches",
        "btn_sky":    "Vuelo — Skyscanner",
        "btn_book":   "Hotel — Booking",
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

# ── Calcul résultats ──────────────────────────
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

# ── Summary ───────────────────────────────────
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
    st.stop()

# ── Grille 3 colonnes avec photos ─────────────
cols = st.columns(3)
for i, r in enumerate(resultats):
    with cols[i % 3]:
        html = render_card(r, T, depart_iata, d1_str, d2_str, adultes, nuits, total_v)
        st.markdown(html, unsafe_allow_html=True)
        # Boutons natifs Streamlit (évite le rendu HTML brut des balises <a>)
        b1, b2 = st.columns(2)
        with b1:
            st.link_button(T["btn_sky"], r["url_sky"], use_container_width=True)
        with b2:
            st.link_button(T["btn_book"], r["url_book"], use_container_width=True)
        st.markdown("<div style='margin-bottom:1.2rem'></div>", unsafe_allow_html=True)
