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
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=Inter:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

  .main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
  }
  .subtitle {
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  .card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
  }
  .card:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.08); }
  .card-fav {
    border: 2px solid #6366f1;
    background: linear-gradient(135deg, #f5f3ff, #eef2ff);
  }
  .dest-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f172a;
  }
  .dest-country { color: #64748b; font-size: 0.85rem; }
  .tag {
    display: inline-block;
    background: #f1f5f9;
    color: #475569;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    margin: 2px 2px 2px 0;
  }
  .price-big {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #0ea5e9;
  }
  .price-label { font-size: 0.75rem; color: #94a3b8; }
  .reste-badge {
    background: #dcfce7;
    color: #166534;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 0.8rem;
    font-weight: 500;
  }
  .fav-badge {
    background: #6366f1;
    color: white;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
  }
  .btn-sky {
    background: linear-gradient(135deg, #0ea5e9, #0284c7);
    color: white !important;
    padding: 8px 18px;
    border-radius: 10px;
    text-decoration: none !important;
    font-weight: 500;
    font-size: 0.85rem;
    display: inline-block;
    margin-right: 8px;
    margin-top: 8px;
  }
  .btn-book {
    background: linear-gradient(135deg, #003580, #0051a5);
    color: white !important;
    padding: 8px 18px;
    border-radius: 10px;
    text-decoration: none !important;
    font-weight: 500;
    font-size: 0.85rem;
    display: inline-block;
    margin-top: 8px;
  }
  .summary-box {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border: 1px solid #bae6fd;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
  }
  .no-result {
    text-align: center;
    padding: 3rem;
    color: #94a3b8;
    font-size: 1.1rem;
  }
  div[data-testid="stSidebarContent"] { padding-top: 1.5rem; }
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
    target = (
        f"https://www.skyscanner.fr/transport/vols/"
        f"{orig.lower()}/{dest.lower()}/{fmt(d1)}/{fmt(d2)}/"
        f"?adults={adultes}&children={enfants}&infants={bebes}"
    )
    encoded = urllib.parse.quote(target, safe='')
    return (
        f"https://tp.media/r?marker={TRAVELPAYOUT_ID}"
        f"&trs=233854&p=4114&u={encoded}&campaign_id=200"
    )

def build_booking_url(destination, d1, d2, adultes, enfants):
    dest_enc = urllib.parse.quote(destination)
    target = (
        f"https://www.booking.com/searchresults.fr.html"
        f"?ss={dest_enc}&checkin={d1}&checkout={d2}"
        f"&group_adults={adultes}&group_children={enfants}&no_rooms=1"
    )
    encoded = urllib.parse.quote(target, safe='')
    return (
        f"https://tp.media/r?marker={TRAVELPAYOUT_ID}"
        f"&trs=233854&p=4&u={encoded}&campaign_id=200"
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
    st.markdown("## 🌍 Pouch Voyage")
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
st.markdown('<div class="main-title">🌍 Pouch Voyage</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Trouvez votre prochaine aventure selon votre budget</div>',
            unsafe_allow_html=True)

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
        fav_badge = '<span class="fav-badge">⭐ Favori</span>' if r["is_favorite"] else ""
        card_class = "card card-fav" if r["is_favorite"] else "card"
        tags_html  = "".join(f'<span class="tag">{t}</span>' for t in r["tags"])

        # Prix live (si clés API dispo)
        live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
        live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits)

        prix_affiche = live_vol["price"] if live_vol else r["prix_estime"]
        prix_label   = "Prix vol (live)" if live_vol else "Prix estimé"
        hotel_line   = f"<br><span style='font-size:0.8rem;color:#64748b'>🏨 {live_hotel['price_per_night']} €/nuit (live)</span>" if live_hotel else ""

        st.markdown(f"""
<div class="{card_class}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <div>
      <span style="font-size:2rem">{r['flag']}</span>
      <span class="dest-name"> {r['nom']}</span>
      <br><span class="dest-country">{r['pays']}</span>
    </div>
    <div style="text-align:right">
      {fav_badge}
      <div class="price-big">{prix_affiche:,} €</div>
      <div class="price-label">{prix_label}{hotel_line}</div>
    </div>
  </div>
  <div style="margin-bottom:8px">{tags_html}</div>
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap">
    <span class="reste-badge">💚 Reste {r['reste']:,} € dans le budget</span>
    <span style="font-size:0.8rem;color:#94a3b8">{r['nuits']} nuits</span>
  </div>
  <div>
    <a href="{r['url_sky']}" target="_blank" class="btn-sky">✈️ Skyscanner</a>
    <a href="{r['url_book']}" target="_blank" class="btn-book">🏨 Booking</a>
  </div>
</div>
""", unsafe_allow_html=True)
