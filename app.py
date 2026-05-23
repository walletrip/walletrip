"""
Pouch Voyage — Application Streamlit
Travelpayout ID: 731169
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
#  CSS — crème / noir / minimaliste
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@300;400;500&display=swap');

  :root {
    --cream:   #F5F0E8;
    --cream2:  #EDE8DE;
    --ink:     #0D0D0D;
    --muted:   #6B6560;
    --border:  #D4CFC6;
    --white:   #FEFCF8;
  }

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--cream) !important;
    color: var(--ink) !important;
  }

  section[data-testid="stMain"],
  .main .block-container {
    background-color: var(--cream) !important;
  }

  /* sidebar */
  section[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--border) !important;
  }
  div[data-testid="stSidebarContent"] { padding: 2rem 1.4rem; }

  /* header */
  header[data-testid="stHeader"] { background: var(--cream) !important; }

  /* titre */
  .logo-wrap {
    display: flex; align-items: center; gap: 16px;
    margin: 2rem 0 0.4rem;
  }
  .main-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem; font-weight: 300;
    color: var(--ink); letter-spacing: 0.02em; line-height: 1;
  }
  .subtitle {
    font-size: 0.88rem; font-weight: 300;
    color: var(--muted); margin-bottom: 2.5rem; letter-spacing: 0.03em;
  }

  /* résumé */
  .summary-box {
    background: var(--cream2);
    border: 1px solid var(--border);
    border-radius: 0;
    padding: 0.8rem 1.2rem;
    margin-bottom: 2rem;
    font-size: 0.85rem; color: var(--muted);
  }
  .summary-box b { color: var(--ink); }

  /* cartes */
  div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    background: var(--white) !important;
    padding: 0.2rem 0.6rem !important;
    transition: border-color 0.2s !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--ink) !important;
  }

  /* texte cartes */
  div[data-testid="stVerticalBlockBorderWrapper"] p,
  div[data-testid="stVerticalBlockBorderWrapper"] span,
  div[data-testid="stVerticalBlockBorderWrapper"] label { color: var(--ink) !important; }
  div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }

  /* metric */
  div[data-testid="stMetric"] {
    background: var(--cream2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 0.6rem 1rem !important;
  }
  div[data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.8rem !important; font-weight: 400 !important;
    color: var(--ink) !important;
  }
  div[data-testid="stMetricLabel"] { font-size: 0.75rem !important; color: var(--muted) !important; }

  /* boutons liens — rectangle plat */
  div[data-testid="stLinkButton"] a {
    background: var(--ink) !important;
    color: var(--cream) !important;
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    font-size: 0.78rem !important; font-weight: 400 !important;
    letter-spacing: 0.06em; text-transform: uppercase;
    padding: 8px 16px !important;
  }
  div[data-testid="stLinkButton"] a:hover {
    background: var(--cream) !important;
    color: var(--ink) !important;
  }

  /* bouton rechercher */
  div[data-testid="stButton"] button {
    background: var(--ink) !important;
    color: var(--cream) !important;
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    font-size: 0.8rem !important; font-weight: 400 !important;
    letter-spacing: 0.06em; text-transform: uppercase;
  }
  div[data-testid="stButton"] button:hover {
    background: var(--cream) !important;
    color: var(--ink) !important;
  }

  /* slider */
  div[data-testid="stSlider"] > div > div > div { background: var(--ink) !important; }

  /* success/alert */
  div[data-testid="stAlert"] {
    background: var(--cream2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    font-size: 0.83rem !important;
  }

  /* info */
  div[data-testid="stInfo"] {
    background: var(--cream2) !important;
    border-color: var(--border) !important;
    border-radius: 0 !important;
    color: var(--muted) !important;
  }

  /* caption global */
  .stCaption, [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }

  /* selectbox / inputs sidebar */
  section[data-testid="stSidebar"] label { color: var(--ink) !important; font-size: 0.82rem !important; }
  section[data-testid="stSidebar"] .stMarkdown p { color: var(--muted) !important; font-size: 0.82rem !important; }

  /* séparateur */
  hr { border-color: var(--border) !important; }

  /* no result */
  .no-result { text-align:center; padding:4rem; color:var(--muted); font-size:0.95rem; font-weight:300; }
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
        "subtitle":     "Trouvez votre prochaine aventure selon votre budget",
        "depart":       "Ville de départ",
        "dates":        "Dates du voyage",
        "budget":       "Budget total (€)",
        "budget_sel":   "Budget : {b:,} €",
        "voyageurs":    "Voyageurs",
        "adultes":      "Adultes",
        "enfants":      "Enfants",
        "bebes":        "Bébés",
        "fav":          "Destination préférée (optionnel)",
        "fav_ph":       "ex : Tokyo, Bali…",
        "search":       "Rechercher",
        "powered":      "Propulsé par Travelpayout",
        "fill_form":    "Remplissez le formulaire et cliquez sur Rechercher.",
        "date_err":     "La date de retour doit être après la date de départ.",
        "found":        "{n} destination(s) · {nuits} nuit(s) · {v} voyageur(s) · Budget {b:,} €",
        "no_result":    "Aucune destination dans ce budget. Essayez d'augmenter le budget.",
        "price_live":   "Vol (prix en direct)",
        "price_est":    "Prix de départ estimé",
        "price_help":   "Indicatif — cliquez Skyscanner pour le prix exact.",
        "hotel_live":   "Hôtel : ~{p:,} €/nuit (en direct)",
        "reste":        "Budget restant après le vol : {r:,} € — {n} nuits",
        "btn_sky":      "Skyscanner",
        "btn_book":     "Booking",
        "fav_label":    "Favori",
    },
    "🇬🇧 English": {
        "subtitle":     "Find your next adventure within your budget",
        "depart":       "Departure city",
        "dates":        "Travel dates",
        "budget":       "Total budget (€)",
        "budget_sel":   "Budget: €{b:,}",
        "voyageurs":    "Travellers",
        "adultes":      "Adults",
        "enfants":      "Children",
        "bebes":        "Infants",
        "fav":          "Preferred destination (optional)",
        "fav_ph":       "e.g. Tokyo, Bali…",
        "search":       "Search",
        "powered":      "Powered by Travelpayout",
        "fill_form":    "Fill in the form and click Search.",
        "date_err":     "Return date must be after departure date.",
        "found":        "{n} destination(s) · {nuits} night(s) · {v} traveller(s) · Budget €{b:,}",
        "no_result":    "No destinations in this budget. Try increasing the budget.",
        "price_live":   "Flight (live price)",
        "price_est":    "Estimated departure price",
        "price_help":   "Indicative — click Skyscanner for exact price.",
        "hotel_live":   "Hotel: ~€{p:,}/night (live)",
        "reste":        "Remaining budget after flight: €{r:,} — {n} nights",
        "btn_sky":      "Skyscanner",
        "btn_book":     "Booking",
        "fav_label":    "Favourite",
    },
    "🇪🇸 Español": {
        "subtitle":     "Encuentra tu próxima aventura según tu presupuesto",
        "depart":       "Ciudad de salida",
        "dates":        "Fechas del viaje",
        "budget":       "Presupuesto total (€)",
        "budget_sel":   "Presupuesto: {b:,} €",
        "voyageurs":    "Viajeros",
        "adultes":      "Adultos",
        "enfants":      "Niños",
        "bebes":        "Bebés",
        "fav":          "Destino preferido (opcional)",
        "fav_ph":       "ej: Tokio, Bali…",
        "search":       "Buscar",
        "powered":      "Desarrollado por Travelpayout",
        "fill_form":    "Rellena el formulario y haz clic en Buscar.",
        "date_err":     "La fecha de regreso debe ser posterior a la de salida.",
        "found":        "{n} destino(s) · {nuits} noche(s) · {v} viajero(s) · Presupuesto {b:,} €",
        "no_result":    "Ningún destino en este presupuesto. Intenta aumentarlo.",
        "price_live":   "Vuelo (precio en directo)",
        "price_est":    "Precio de salida estimado",
        "price_help":   "Indicativo — haz clic en Skyscanner para el precio exacto.",
        "hotel_live":   "Hotel: ~{p:,} €/noche (en directo)",
        "reste":        "Presupuesto restante tras el vuelo: {r:,} € — {n} noches",
        "btn_sky":      "Skyscanner",
        "btn_book":     "Booking",
        "fav_label":    "Favorito",
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
    # Sélecteur de langue EN PREMIER
    lang_key = st.selectbox("", list(LANGS.keys()), label_visibility="collapsed")
    T = LANGS[lang_key]

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:1rem 0 0.2rem">
      {LOGO_SVG.format(w=28)}
      <span style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;
                   font-weight:400;color:#0D0D0D;letter-spacing:0.04em">
        Pouch Voyage
      </span>
    </div>
    <hr style="margin:0.6rem 0 1.2rem">
    """, unsafe_allow_html=True)

    ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
    ville_idx = st.selectbox(T["depart"], range(len(ville_options)),
                              format_func=lambda i: ville_options[i])
    depart_iata = VILLES_DEPART[ville_idx]["iata"]

    st.caption(T["dates"])
    col1, col2 = st.columns(2)
    with col1:
        d1 = st.date_input("↗", value=date.today() + timedelta(days=30),
                            min_value=date.today(), label_visibility="collapsed")
    with col2:
        d2 = st.date_input("↙", value=date.today() + timedelta(days=37),
                            min_value=date.today(), label_visibility="collapsed")
    st.caption(f"{d1.strftime('%d/%m/%Y')} → {d2.strftime('%d/%m/%Y')}")

    st.caption(T["budget"])
    budget = st.slider("budget", min_value=500, max_value=10000,
                        value=3000, step=100, label_visibility="collapsed")
    st.caption(T["budget_sel"].format(b=budget))

    st.caption(T["voyageurs"])
    c1, c2, c3 = st.columns(3)
    with c1:
        adultes = st.number_input(T["adultes"], min_value=1, max_value=9, value=2, step=1)
    with c2:
        enfants = st.number_input(T["enfants"], min_value=0, max_value=9, value=0, step=1)
    with c3:
        bebes = st.number_input(T["bebes"], min_value=0, max_value=9, value=0, step=1)

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

nuits = (d2 - d1).days
if nuits <= 0:
    st.error(T["date_err"])
    st.stop()

d1_str    = d1.strftime("%Y-%m-%d")
d2_str    = d2.strftime("%Y-%m-%d")
fav_lower = fav.lower().strip()

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
        "nuits": nuits,
        "reste": budget - prix_est,
        "score": score,
        "is_favorite": score >= 10,
        "url_sky":  build_skyscanner_url(depart_iata, dest["iata"], d1_str, d2_str, adultes, enfants, bebes),
        "url_book": build_booking_url(dest["booking_id"], d1_str, d2_str, adultes, enfants),
    })

resultats.sort(key=lambda x: (-x["score"], x["prix_estime"]))
resultats = resultats[:12]

# ── Résumé ────────────────────────────────────
total_v = adultes + enfants + bebes
st.markdown(f"""
<div class="summary-box">
  {T["found"].format(n=len(resultats), nuits=nuits, v=total_v, b=budget)}
</div>
""", unsafe_allow_html=True)

if not resultats:
    st.markdown(f'<div class="no-result">{T["no_result"]}</div>', unsafe_allow_html=True)
    st.stop()

# ── Grille ────────────────────────────────────
cols = st.columns(2)
for i, r in enumerate(resultats):
    with cols[i % 2]:
        with st.container(border=True):
            fav_txt = f" — {T['fav_label']}" if r["is_favorite"] else ""
            st.markdown(f"{r['flag']} **{r['nom']}**{fav_txt}")
            st.caption(r["pays"])

            live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
            live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits)

            if live_vol:
                st.metric(T["price_live"], f"{live_vol['price']:,} €")
            else:
                st.metric(T["price_est"], f"{r['prix_estime']:,} €", help=T["price_help"])

            if live_hotel:
                st.caption(T["hotel_live"].format(p=live_hotel["price_per_night"]))

            st.caption("  ·  ".join(r["tags"]))
            st.success(T["reste"].format(r=r["reste"], n=r["nuits"]))

            c1, c2 = st.columns(2)
            with c1:
                st.link_button(T["btn_sky"], r["url_sky"], use_container_width=True)
            with c2:
                st.link_button(T["btn_book"], r["url_book"], use_container_width=True)
