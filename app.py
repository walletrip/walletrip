"""
🌍 Pouch Voyage — Application Streamlit
Convertie depuis Flask | Travelpayout ID: 731169
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
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS CUSTOM
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display&display=swap');

  /* ── palette vert forêt ── */
  :root {
    --forest:      #1B3A2D;
    --forest-deep: #122A20;
    --forest-card: #1E3F30;
    --gold:        #C9A84C;
    --gold-light:  #E8D5A3;
    --ink:         #0A0A0A;
    --text-light:  #D4E4DC;
    --muted:       #7FA992;
    --border:      #2E5240;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--forest) !important;
    color: var(--ink);
  }

  /* fond principal */
  .main .block-container {
    background-color: var(--forest) !important;
  }
  section[data-testid="stMain"] {
    background-color: var(--forest) !important;
  }

  /* sidebar */
  section[data-testid="stSidebar"] {
    background: var(--forest-deep) !important;
    border-right: 1px solid var(--border) !important;
  }
  div[data-testid="stSidebarContent"] { padding: 2rem 1.2rem; }
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] .stMarkdown,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span { color: var(--text-light) !important; }
  section[data-testid="stSidebar"] input,
  section[data-testid="stSidebar"] select {
    background: var(--forest-card) !important;
    color: var(--text-light) !important;
    border-color: var(--border) !important;
  }

  /* header Streamlit */
  header[data-testid="stHeader"] {
    background: var(--forest-deep) !important;
    border-bottom: 1px solid var(--border) !important;
  }

  /* logo + titre */
  .logo-wrap {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0.3rem;
    margin-top: 1.5rem;
  }
  .logo-svg { flex-shrink: 0; }
  .main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: var(--gold-light);
    letter-spacing: -0.02em;
    line-height: 1;
  }
  .subtitle {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
    margin-bottom: 2.5rem;
    margin-left: 2px;
  }

  /* résumé */
  .summary-box {
    background: var(--forest-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    margin-bottom: 2rem;
    font-size: 0.9rem;
    color: var(--text-light);
  }

  /* pas de résultat */
  .no-result {
    text-align: center;
    padding: 4rem;
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
  }

  /* boutons */
  div[data-testid="stLinkButton"] a {
    background: var(--gold) !important;
    color: var(--forest-deep) !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 6px 14px !important;
    letter-spacing: 0.01em;
  }
  div[data-testid="stLinkButton"] a:hover {
    background: var(--gold-light) !important;
  }

  /* bouton rechercher */
  div[data-testid="stButton"] button {
    background: var(--gold) !important;
    color: var(--forest-deep) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
  }

  /* slider */
  div[data-testid="stSlider"] > div > div > div {
    background: var(--gold) !important;
  }

  /* metric */
  div[data-testid="stMetric"] {
    background: var(--forest-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.7rem 1rem;
  }
  div[data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.6rem !important;
    color: var(--gold-light) !important;
  }
  div[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    color: var(--muted) !important;
  }

  /* success / alert */
  div[data-testid="stAlert"] {
    background: var(--forest-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-light) !important;
    font-size: 0.85rem !important;
  }

  /* cartes résultats */
  div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: var(--forest-card) !important;
    padding: 0.2rem 0.4rem !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--gold) !important;
    box-shadow: 0 4px 24px rgba(201,168,76,0.12) !important;
  }

  /* texte dans les cartes */
  div[data-testid="stVerticalBlockBorderWrapper"] p,
  div[data-testid="stVerticalBlockBorderWrapper"] span,
  div[data-testid="stVerticalBlockBorderWrapper"] label,
  div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown {
    color: var(--text-light) !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"] strong {
    color: var(--gold-light) !important;
  }

  /* caption général */
  .stCaption, [data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
  }

  /* info box */
  div[data-testid="stInfo"] {
    background: var(--forest-card) !important;
    border-color: var(--border) !important;
    color: var(--text-light) !important;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────
TRAVELPAYOUT_ID = "731169"

SKYSCANNER_API_KEY = st.secrets.get("SKYSCANNER_API_KEY", "")
BOOKING_API_KEY    = st.secrets.get("BOOKING_API_KEY", "")
SKYSCANNER_HOST    = "skyscanner50.p.rapidapi.com"
BOOKING_HOST       = "booking-com15.p.rapidapi.com"

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
        dest_id   = results[0]["dest_id"]
        dest_type = results[0]["dest_type"]
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
#  SIDEBAR — FORMULAIRE
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:0.5rem">
  <svg width="32" height="32" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4" y="14" width="36" height="26" rx="6" fill="#1E3F30" stroke="#C9A84C" stroke-width="1.8"/>
    <path d="M4 21h36" stroke="#C9A84C" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M4 14c0-3.3 2.7-6 6-6h20c3.3 0 6 2.7 6 6" stroke="#C9A84C" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    <rect x="28" y="25" width="14" height="9" rx="4.5" fill="#C9A84C"/>
    <circle cx="35" cy="29.5" r="2" fill="#1E3F30"/>
    <g transform="translate(30,8) rotate(-30)">
      <path d="M0 0 L8 3 L0 6 L1.5 3 Z" fill="#E8D5A3"/>
    </g>
  </svg>
  <span style="font-family:'DM Serif Display',serif;font-size:1.1rem;color:#1C2421;letter-spacing:-0.01em">Pouch Voyage</span>
</div>
""", unsafe_allow_html=True)
    st.markdown("---")

    ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
    ville_idx = st.selectbox("✈️ Ville de départ", range(len(ville_options)),
                              format_func=lambda i: ville_options[i])
    depart_iata = VILLES_DEPART[ville_idx]["iata"]

    st.markdown("**📅 Dates du voyage**")
    col1, col2 = st.columns(2)
    with col1:
        d1 = st.date_input("Départ", value=date.today() + timedelta(days=30),
                            min_value=date.today(), label_visibility="collapsed")
    with col2:
        d2 = st.date_input("Retour", value=date.today() + timedelta(days=37),
                            min_value=date.today(), label_visibility="collapsed")
    st.caption(f"Départ : {d1.strftime('%d/%m/%Y')}  →  Retour : {d2.strftime('%d/%m/%Y')}")

    st.markdown("**💰 Budget total (€)**")
    budget = st.slider("Budget", min_value=500, max_value=10000,
                        value=3000, step=100, label_visibility="collapsed")
    st.caption(f"Budget sélectionné : **{budget:,} €**")

    st.markdown("**👥 Voyageurs**")
    c1, c2, c3 = st.columns(3)
    with c1:
        adultes = st.number_input("Adultes", min_value=1, max_value=9, value=2, step=1)
    with c2:
        enfants = st.number_input("Enfants", min_value=0, max_value=9, value=0, step=1)
    with c3:
        bebes = st.number_input("Bébés", min_value=0, max_value=9, value=0, step=1)

    fav = st.text_input("🔍 Destination préférée (optionnel)", placeholder="ex: Tokyo, Bali…")

    chercher = st.button("🔎 Rechercher", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("Powered by Travelpayout · ID 731169")

# ─────────────────────────────────────────────
#  CONTENU PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="logo-wrap">
  <svg class="logo-svg" width="52" height="52" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4" y="14" width="36" height="26" rx="6" fill="#1E3F30" stroke="#C9A84C" stroke-width="1.8"/>
    <path d="M4 21h36" stroke="#C9A84C" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M4 14c0-3.3 2.7-6 6-6h20c3.3 0 6 2.7 6 6" stroke="#C9A84C" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    <rect x="28" y="25" width="14" height="9" rx="4.5" fill="#C9A84C"/>
    <circle cx="35" cy="29.5" r="2" fill="#1E3F30"/>
    <g transform="translate(30,8) rotate(-30)">
      <path d="M0 0 L8 3 L0 6 L1.5 3 Z" fill="#E8D5A3"/>
      <path d="M1 1.5 L-3 3.5 L-2 3 Z" fill="#C9A84C"/>
      <path d="M5 2.5 L3 5.5 L3.5 3 Z" fill="#C9A84C"/>
    </g>
  </svg>
  <div class="main-title">Pouch Voyage</div>
</div>
<div class="subtitle">Trouvez votre prochaine aventure selon votre budget</div>
""", unsafe_allow_html=True)

if not chercher:
    st.info("👈 Remplissez le formulaire dans la barre latérale et cliquez sur **Rechercher**.")
    st.stop()

# Validation des dates
nuits = (d2 - d1).days
if nuits <= 0:
    st.error("⚠️ La date de retour doit être après la date de départ.")
    st.stop()

d1_str = d1.strftime("%Y-%m-%d")
d2_str = d2.strftime("%Y-%m-%d")
fav_lower = fav.lower().strip()

# ── Calcul des résultats ──────────────────────
resultats = []
for dest in DESTINATIONS:
    prix_est = prix_total(dest["prix_base"], adultes, enfants, bebes)
    if prix_est > budget:
        continue

    score = 0
    if prix_est <= budget * 0.75:
        score += 2
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
total_voyageurs = adultes + enfants + bebes
st.markdown(f"""
<div class="summary-box">
  <b>{len(resultats)} destination(s) trouvée(s)</b> &nbsp;·&nbsp;
  {nuits} nuit(s) &nbsp;·&nbsp;
  {total_voyageurs} voyageur(s) ({adultes} adulte(s){f', {enfants} enfant(s)' if enfants else ''}{f', {bebes} bébé(s)' if bebes else ''}) &nbsp;·&nbsp;
  Budget : <b>{budget:,} €</b>
</div>
""", unsafe_allow_html=True)

if not resultats:
    st.markdown('<div class="no-result">😔 Aucune destination ne correspond à votre budget.<br>Essayez d\'augmenter le budget ou de changer les dates.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Grille de résultats ───────────────────────
cols = st.columns(2)
for i, r in enumerate(resultats):
    col = cols[i % 2]
    with col:
        with st.container(border=True):

            # Titre + pays
            titre = f"{'⭐ ' if r['is_favorite'] else ''}{r['flag']} **{r['nom']}**"
            st.markdown(titre)
            st.caption(r["pays"])

            # Prix live si dispo, sinon estimé
            live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
            live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits)

            if live_vol:
                st.metric("✈️ Vol (prix en direct)", f"{live_vol['price']:,} €")
            else:
                st.metric("✈️ Prix de départ estimé", f"{r['prix_estime']:,} €",
                          help="Prix indicatif basé sur les tarifs habituels. Cliquez sur Skyscanner pour le prix exact.")

            if live_hotel:
                st.caption(f"🏨 Hôtel : environ {live_hotel['price_per_night']:,} €/nuit (en direct)")

            # Tags
            st.caption("  •  ".join(r["tags"]))

            # Budget restant
            st.success(f"💚 Il vous resterait **{r['reste']:,} €** de budget après le vol — {r['nuits']} nuits")

            # Boutons
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("✈️ Voir sur Skyscanner", r["url_sky"], use_container_width=True)
            with c2:
                st.link_button("🏨 Voir sur Booking", r["url_book"], use_container_width=True)
