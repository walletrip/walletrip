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
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  PHOTOS UNSPLASH
# ─────────────────────────────────────────────
DEST_PHOTOS = {
    "Lisbonne":       "https://images.unsplash.com/photo-1558370781-d6196949e317?w=800&q=80",
    "Barcelone":      "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=800&q=80",
    "Madrid":         "https://images.unsplash.com/photo-1543783207-ec64e4d95325?w=800&q=80",
    "Rome":           "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800&q=80",
    "Venise":         "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=800&q=80",
    "Florence":       "https://images.unsplash.com/photo-1541370976299-4d24be63289f?w=800&q=80",
    "Nice":           "https://images.unsplash.com/photo-1491166617655-0723a0948b8b?w=800&q=80",
    "Santorin":       "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
    "Athènes":        "https://images.unsplash.com/photo-1555993539-1732b0258235?w=800&q=80",
    "Crète":          "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=800&q=80",
    "Dubrovnik":      "https://images.unsplash.com/photo-1555990538-c0a6a2e8e1e8?w=800&q=80",
    "Split":          "https://images.unsplash.com/photo-1564760290292-23341e4df6ec?w=800&q=80",
    "Prague":         "https://images.unsplash.com/photo-1519677100203-a0e668c92439?w=800&q=80",
    "Budapest":       "https://images.unsplash.com/photo-1541849546-216549ae216d?w=800&q=80",
    "Amsterdam":      "https://images.unsplash.com/photo-1534351590666-13e3e96b5017?w=800&q=80",
    "Berlin":         "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=800&q=80",
    "Munich":         "https://images.unsplash.com/photo-1595867818082-083862f3d630?w=800&q=80",
    "Zurich":         "https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=800&q=80",
    "Interlaken":     "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    "Stockholm":      "https://images.unsplash.com/photo-1509356843151-3e7d96241e11?w=800&q=80",
    "Copenhague":     "https://images.unsplash.com/photo-1513622470522-26c3c8a854bc?w=800&q=80",
    "Oslo":           "https://images.unsplash.com/photo-1531435338678-4ef2b632e95a?w=800&q=80",
    "Bergen":         "https://images.unsplash.com/photo-1601439678777-b2b3c56fa627?w=800&q=80",
    "Helsinki":       "https://images.unsplash.com/photo-1559598467-f8b76c8155d0?w=800&q=80",
    "Reykjavik":      "https://images.unsplash.com/photo-1474690870753-1b92efa1f2d8?w=800&q=80",
    "Cracovie":       "https://images.unsplash.com/photo-1584892941636-f1e5686a7247?w=800&q=80",
    "Bucarest":       "https://images.unsplash.com/photo-1584811644165-33db418a4c73?w=800&q=80",
    "Istanbul":       "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800&q=80",
    "Cappadoce":      "https://images.unsplash.com/photo-1570856686220-c2e416f39dac?w=800&q=80",
    "Londres":        "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=800&q=80",
    "Édimbourg":      "https://images.unsplash.com/photo-1506377872008-6645d9d29ef7?w=800&q=80",
    "Dublin":         "https://images.unsplash.com/photo-1549918864-48ac978761a4?w=800&q=80",
    "La Valette":     "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
    "Tokyo":          "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80",
    "Kyoto":          "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800&q=80",
    "Osaka":          "https://images.unsplash.com/photo-1590559899731-a382839e5549?w=800&q=80",
    "Bangkok":        "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=800&q=80",
    "Chiang Mai":     "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800&q=80",
    "Phuket":         "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=800&q=80",
    "Koh Samui":      "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800&q=80",
    "Hanoï":          "https://images.unsplash.com/photo-1555348268-f2b67b58ca3b?w=800&q=80",
    "Ho Chi Minh":    "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=800&q=80",
    "Hội An":         "https://images.unsplash.com/photo-1557750255-c76072a7aad1?w=800&q=80",
    "Da Nang":        "https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=800&q=80",
    "Siem Reap":      "https://images.unsplash.com/photo-1508159452718-d22f6734a236?w=800&q=80",
    "Bagan":          "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=800&q=80",
    "Luang Prabang":  "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800&q=80",
    "Kuala Lumpur":   "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=800&q=80",
    "Singapour":      "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&q=80",
    "Bali":           "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80",
    "Lombok":         "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800&q=80",
    "Palawan":        "https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=800&q=80",
    "Goa":            "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&q=80",
    "Jaipur":         "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800&q=80",
    "Kerala":         "https://images.unsplash.com/photo-1609766418204-94aae0ecfdfc?w=800&q=80",
    "Katmandou":      "https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=800&q=80",
    "Malé":           "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    "Pékin":          "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?w=800&q=80",
    "Séoul":          "https://images.unsplash.com/photo-1538485399081-7191377e8241?w=800&q=80",
    "Dubaï":          "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
    "Pétra":          "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80",
    "Samarcande":     "https://images.unsplash.com/photo-1596397249129-c7a8f9bdf9b6?w=800&q=80",
    "Tbilissi":       "https://images.unsplash.com/photo-1565008576549-57f8b4a16b5b?w=800&q=80",
    "New York":       "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800&q=80",
    "Los Angeles":    "https://images.unsplash.com/photo-1580655653885-65763b2597d1?w=800&q=80",
    "Miami":          "https://images.unsplash.com/photo-1514214246283-d427a95c5d2f?w=800&q=80",
    "San Francisco":  "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800&q=80",
    "Las Vegas":      "https://images.unsplash.com/photo-1605833556294-ea5c7a74f57d?w=800&q=80",
    "Hawaii":         "https://images.unsplash.com/photo-1507876466758-e54a1a9c47cf?w=800&q=80",
    "Montréal":       "https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=800&q=80",
    "Vancouver":      "https://images.unsplash.com/photo-1559511260-66a654ae982a?w=800&q=80",
    "Mexico":         "https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800&q=80",
    "Cancún":         "https://images.unsplash.com/photo-1552074284-5e88ef1aef18?w=800&q=80",
    "La Havane":      "https://images.unsplash.com/photo-1500759285222-a95626359a64?w=800&q=80",
    "Carthagène":     "https://images.unsplash.com/photo-1576502200272-341a4b8d5e5d?w=800&q=80",
    "Medellín":       "https://images.unsplash.com/photo-1591087952234-e7e62f7c0513?w=800&q=80",
    "Cusco":          "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=800&q=80",
    "Lima":           "https://images.unsplash.com/photo-1531968455001-5c5272a41129?w=800&q=80",
    "Rio de Janeiro": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800&q=80",
    "Buenos Aires":   "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=800&q=80",
    "Patagonie":      "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&q=80",
    "Atacama":        "https://images.unsplash.com/photo-1534543099237-81b7f7d43688?w=800&q=80",
    "Galápagos":      "https://images.unsplash.com/photo-1548759806-821cbf3cd0b8?w=800&q=80",
    "Marrakech":      "https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=800&q=80",
    "Fès":            "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=800&q=80",
    "Le Caire":       "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",
    "Louxor":         "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",
    "Zanzibar":       "https://images.unsplash.com/photo-1586861203927-800a5acddfbe?w=800&q=80",
    "Serengeti":      "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&q=80",
    "Nairobi":        "https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800&q=80",
    "Le Cap":         "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=800&q=80",
    "Victoria Falls": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80",
    "Mahé":           "https://images.unsplash.com/photo-1573551089778-46a7abc39d9f?w=800&q=80",
    "Île Maurice":    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80",
    "Cap-Vert":       "https://images.unsplash.com/photo-1580094333632-438bdc04f79f?w=800&q=80",
    "Dakar":          "https://images.unsplash.com/photo-1574082595171-4a1e9b40af52?w=800&q=80",
    "Sydney":         "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=800&q=80",
    "Melbourne":      "https://images.unsplash.com/photo-1514395462725-fb4566210144?w=800&q=80",
    "Cairns":         "https://images.unsplash.com/photo-1587139223877-04edf6e50197?w=800&q=80",
    "Queenstown":     "https://images.unsplash.com/photo-1507699622108-4be3abd695ad?w=800&q=80",
    "Fidji":          "https://images.unsplash.com/photo-1590523741831-ab7e8b8f9c7f?w=800&q=80",
    "Bora Bora":      "https://images.unsplash.com/photo-1589197331516-4d84b72ebde3?w=800&q=80",
}

# ─────────────────────────────────────────────
#  CSS
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

  /* ── Photo accueil haute résolution ── */
  .hero-photo { height: 340px !important; }

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

  .dest-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 0.9rem; }
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
  .dest-nights { font-size: 0.72rem; color: var(--muted); text-align: right; letter-spacing: 0.05em; }
  .dest-reste { font-size: 0.72rem; color: var(--gold); letter-spacing: 0.05em; margin-top: 2px; }
  .dest-hotel { font-size: 0.72rem; color: var(--muted); letter-spacing: 0.05em; margin-bottom: 0.9rem; font-style: italic; }

  .btn-row { display: flex; gap: 8px; }
  .btn-aff {
    flex: 1; display: block; text-align: center; padding: 9px 0;
    font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;
    text-decoration: none !important; border: 1px solid var(--ink);
    color: var(--ink) !important; background: transparent;
    transition: background 0.2s, color 0.2s; font-family: 'Inter', sans-serif;
  }
  .btn-aff:hover { background: var(--ink); color: var(--cream) !important; }
  .btn-aff-dark { background: var(--ink); color: var(--cream) !important; }
  .btn-aff-dark:hover { background: var(--cream2); color: var(--ink) !important; border-color: var(--ink); }

  div[data-testid="stButton"] button {
    background: var(--ink) !important; color: var(--cream) !important;
    border: 1px solid var(--ink) !important; border-radius: 0 !important;
    font-size: 0.75rem !important; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 400 !important;
  }
  div[data-testid="stButton"] button:hover { background: var(--cream2) !important; color: var(--ink) !important; }

  div[data-testid="stLinkButton"] a {
    background: var(--ink) !important; color: var(--cream) !important;
    border: 1px solid var(--ink) !important; border-radius: 0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.72rem !important;
    font-weight: 400 !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important; padding: 9px 12px !important;
    width: 100% !important; display: block !important; text-align: center !important;
    transition: background 0.2s ease, color 0.2s ease !important;
  }
  div[data-testid="stLinkButton"] a:hover { background: var(--cream2) !important; color: var(--ink) !important; }

  div[data-testid="stSlider"] > div > div > div { background: var(--ink) !important; }

  .msg-sage {
    background: #EEF2EE; border-left: 2px solid #7A9E7E; color: #4A6E4E;
    font-size: 0.82rem; letter-spacing: 0.05em; padding: 0.7rem 1rem;
    margin: 0.5rem 0; font-style: italic;
  }

  .no-result { text-align:center; padding:5rem 2rem; color:var(--muted); font-size:0.9rem; font-weight:300; letter-spacing:0.05em; }

  div[data-testid="stAlert"] {
    background: #EEF2EE !important; border: 1px solid #7A9E7E !important;
    border-radius: 0 !important; color: #4A6E4E !important; font-size: 0.82rem !important;
  }
  div[data-testid="stAlert"] p { color: #4A6E4E !important; }
  .stCaption, [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }
  hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

  .powered { font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--border); margin-top: 1.5rem; text-align: center; }

  /* ── Vol retour backpacker ── */
  .return-flight-row {
    background: var(--cream2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.4rem; margin-bottom: 8px; gap: 1rem;
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
        "tab_cost":    "❧  Coût de la vie",
        "cost_title":  "Coût de la vie par jour",
        "cost_sub":    "Entrez une ville pour estimer votre budget quotidien",
        "cost_input":  "Ville de destination",
        "cost_ph":     "ex : Bangkok, Lisbonne, New York…",
        "cost_btn":    "Calculer",
        "cost_ndays":  "Nombre de jours",
        "cost_total":  "Budget total estimé",
        "cost_src":    "Source : Numbeo (données moyennes)",
        "cost_err":    "Ville introuvable. Essayez un autre nom.",
        "cost_cats": {"repas":"Repas","transport":"Transport","logement":"Logement","loisirs":"Loisirs & divers"},
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
        "btn_book":   "⌂  Booking",
        "fav_label":  "Favori",
        "per_pax":    "pour {v} voyageur(s)",
        "tab_weather": "☁  Météo",
        "tab_bpack":   "🎒  Backpacker",
        "wx_title":    "Météo par destination",
        "wx_sub":      "Entrez une ville pour connaître la météo actuelle",
        "wx_input":    "Ville",
        "wx_ph":       "ex : Tokyo, Lisbonne, Dubaï…",
        "wx_btn":      "Voir la météo",
        "wx_feels":    "Ressenti",
        "wx_humidity": "Humidité",
        "wx_wind":     "Vent",
        "wx_sunrise":  "Lever",
        "wx_sunset":   "Coucher",
        "wx_err":      "Ville introuvable. Vérifiez l'orthographe.",
        "wx_prompt":   "Tapez une ville et cliquez sur Voir la météo.",
        "wx_src":      "Source : Open-Meteo + OpenStreetMap (données temps réel)",
        "bp_title":    "Itinéraire Backpacker",
        "bp_sub":      "Entrez votre budget total et vos préférences — on construit votre tour du monde",
        "bp_budget":   "Budget total (€)",
        "bp_days":     "Nombre de jours",
        "bp_style":    "Style de voyage",
        "bp_styles":   ["Économique 🌿", "Équilibré ⚖️", "Confort 🛎"],
        "bp_region":   "Régions préférées (optionnel)",
        "bp_regions":  ["Asie du Sud-Est", "Europe de l'Est", "Amérique Latine", "Afrique", "Océanie", "Moyen-Orient"],
        "bp_btn":      "Générer l'itinéraire",
        "bp_prompt":   "Remplissez les champs et générez votre itinéraire.",
        "bp_grand":    "Total itinéraire",
        "bp_warning":  "Budget insuffisant pour un itinéraire multi-pays. Augmentez le budget ou réduisez les jours.",
        "bp_src":      "Estimations basées sur données Numbeo & prix moyens compagnies aériennes",
        "bp_return_label": "Vol retour",
        "bp_return_to":    "Retour vers",
        "bp_return_est":   "Vol estimé",
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
        "tab_cost":    "❧  Cost of living",
        "cost_title":  "Daily cost of living",
        "cost_sub":    "Enter a city to estimate your daily budget",
        "cost_input":  "Destination city",
        "cost_ph":     "e.g. Bangkok, Lisbon, New York…",
        "cost_btn":    "Calculate",
        "cost_ndays":  "Number of days",
        "cost_total":  "Estimated total budget",
        "cost_src":    "Source: Numbeo (average data)",
        "cost_err":    "City not found. Try another name.",
        "cost_cats": {"repas":"Meals","transport":"Transport","logement":"Accommodation","loisirs":"Leisure & misc"},
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
        "btn_book":   "⌂  Booking",
        "fav_label":  "Favourite",
        "per_pax":    "for {v} traveller(s)",
        "tab_weather": "☁  Weather",
        "tab_bpack":   "🎒  Backpacker",
        "wx_title":    "Weather by destination",
        "wx_sub":      "Enter a city to check current weather",
        "wx_input":    "City",
        "wx_ph":       "e.g. Tokyo, Lisbon, Dubai…",
        "wx_btn":      "Check weather",
        "wx_feels":    "Feels like",
        "wx_humidity": "Humidity",
        "wx_wind":     "Wind",
        "wx_sunrise":  "Sunrise",
        "wx_sunset":   "Sunset",
        "wx_err":      "City not found. Check spelling.",
        "wx_prompt":   "Enter a city and click Check weather.",
        "wx_src":      "Source: Open-Meteo + OpenStreetMap (live data)",
        "bp_title":    "Backpacker Itinerary",
        "bp_sub":      "Enter your total budget and preferences — we'll build your world trip",
        "bp_budget":   "Total budget (€)",
        "bp_days":     "Number of days",
        "bp_style":    "Travel style",
        "bp_styles":   ["Budget 🌿", "Balanced ⚖️", "Comfort 🛎"],
        "bp_regions":  ["Southeast Asia", "Eastern Europe", "Latin America", "Africa", "Oceania", "Middle East"],
        "bp_region":   "Preferred regions (optional)",
        "bp_btn":      "Generate itinerary",
        "bp_prompt":   "Fill in the fields and generate your itinerary.",
        "bp_grand":    "Total itinerary",
        "bp_warning":  "Budget too low for a multi-country itinerary. Increase budget or reduce days.",
        "bp_src":      "Estimates based on Numbeo data & average airline prices",
        "bp_return_label": "Return flight",
        "bp_return_to":    "Return to",
        "bp_return_est":   "Estimated flight",
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
        "tab_cost":    "❧  Coste de vida",
        "cost_title":  "Coste de vida por día",
        "cost_sub":    "Introduce una ciudad para estimar tu presupuesto diario",
        "cost_input":  "Ciudad de destino",
        "cost_ph":     "ej: Bangkok, Lisboa, Nueva York…",
        "cost_btn":    "Calcular",
        "cost_ndays":  "Número de días",
        "cost_total":  "Presupuesto total estimado",
        "cost_src":    "Fuente: Numbeo (datos medios)",
        "cost_err":    "Ciudad no encontrada. Prueba otro nombre.",
        "cost_cats": {"repas":"Comidas","transport":"Transporte","logement":"Alojamiento","loisirs":"Ocio y varios"},
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
        "btn_book":   "⌂  Booking",
        "fav_label":  "Favorito",
        "per_pax":    "para {v} viajero(s)",
        "tab_weather": "☁  Tiempo",
        "tab_bpack":   "🎒  Backpacker",
        "wx_title":    "Tiempo por destino",
        "wx_sub":      "Introduce una ciudad para ver el tiempo actual",
        "wx_input":    "Ciudad",
        "wx_ph":       "ej: Tokio, Lisboa, Dubái…",
        "wx_btn":      "Ver el tiempo",
        "wx_feels":    "Sensación",
        "wx_humidity": "Humedad",
        "wx_wind":     "Viento",
        "wx_sunrise":  "Amanecer",
        "wx_sunset":   "Atardecer",
        "wx_err":      "Ciudad no encontrada. Verifica la ortografía.",
        "wx_prompt":   "Introduce una ciudad y haz clic en Ver el tiempo.",
        "wx_src":      "Fuente: Open-Meteo + OpenStreetMap (datos en tiempo real)",
        "bp_title":    "Itinerario Mochilero",
        "bp_sub":      "Introduce tu presupuesto total y preferencias — construimos tu viaje al mundo",
        "bp_budget":   "Presupuesto total (€)",
        "bp_days":     "Número de días",
        "bp_style":    "Estilo de viaje",
        "bp_styles":   ["Económico 🌿", "Equilibrado ⚖️", "Confort 🛎"],
        "bp_regions":  ["Asia del Sudeste", "Europa del Este", "América Latina", "África", "Oceanía", "Oriente Medio"],
        "bp_region":   "Regiones preferidas (opcional)",
        "bp_btn":      "Generar itinerario",
        "bp_prompt":   "Rellena los campos y genera tu itinerario.",
        "bp_grand":    "Total itinerario",
        "bp_warning":  "Presupuesto insuficiente. Aumenta el presupuesto o reduce los días.",
        "bp_src":      "Estimaciones basadas en datos de Numbeo y precios medios de aerolíneas",
        "bp_return_label": "Vuelo de regreso",
        "bp_return_to":    "Regreso a",
        "bp_return_est":   "Vuelo estimado",
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
    {"flag":"🇵🇹","nom":"Lisbonne","pays":"Portugal","iata":"LIS","booking_id":"Lisbon","tags":["Histoire","Fado","Gastronomie"],"prix_base":700},
    {"flag":"🇪🇸","nom":"Barcelone","pays":"Espagne","iata":"BCN","booking_id":"Barcelona","tags":["Architecture","Plage","Vie nocturne"],"prix_base":900},
    {"flag":"🇪🇸","nom":"Madrid","pays":"Espagne","iata":"MAD","booking_id":"Madrid","tags":["Musées","Gastronomie","Culture"],"prix_base":850},
    {"flag":"🇮🇹","nom":"Rome","pays":"Italie","iata":"FCO","booking_id":"Rome","tags":["Histoire","Art","Gastronomie"],"prix_base":950},
    {"flag":"🇮🇹","nom":"Venise","pays":"Italie","iata":"VCE","booking_id":"Venice","tags":["Romance","Architecture","Art"],"prix_base":1100},
    {"flag":"🇮🇹","nom":"Florence","pays":"Italie","iata":"FLR","booking_id":"Florence","tags":["Art","Renaissance","Gastronomie"],"prix_base":900},
    {"flag":"🇫🇷","nom":"Nice","pays":"France","iata":"NCE","booking_id":"Nice","tags":["Plage","Côte d'Azur","Gastronomie"],"prix_base":1000},
    {"flag":"🇬🇷","nom":"Santorin","pays":"Grèce","iata":"JTR","booking_id":"Santorini","tags":["Romance","Mer","Gastronomie"],"prix_base":1600},
    {"flag":"🇬🇷","nom":"Athènes","pays":"Grèce","iata":"ATH","booking_id":"Athens","tags":["Histoire","Mythologie","Culture"],"prix_base":750},
    {"flag":"🇬🇷","nom":"Crète","pays":"Grèce","iata":"HER","booking_id":"Crete","tags":["Plage","Histoire","Nature"],"prix_base":800},
    {"flag":"🇭🇷","nom":"Dubrovnik","pays":"Croatie","iata":"DBV","booking_id":"Dubrovnik","tags":["Mer","Histoire","Beauté"],"prix_base":1000},
    {"flag":"🇨🇿","nom":"Prague","pays":"République Tchèque","iata":"PRG","booking_id":"Prague","tags":["Architecture","Bière","Histoire"],"prix_base":600},
    {"flag":"🇭🇺","nom":"Budapest","pays":"Hongrie","iata":"BUD","booking_id":"Budapest","tags":["Thermes","Architecture","Nuit"],"prix_base":550},
    {"flag":"🇦🇹","nom":"Vienne","pays":"Autriche","iata":"VIE","booking_id":"Vienna","tags":["Musique","Musées","Architecture"],"prix_base":900},
    {"flag":"🇳🇱","nom":"Amsterdam","pays":"Pays-Bas","iata":"AMS","booking_id":"Amsterdam","tags":["Canaux","Musées","Vélo"],"prix_base":1100},
    {"flag":"🇩🇪","nom":"Berlin","pays":"Allemagne","iata":"BER","booking_id":"Berlin","tags":["Histoire","Art","Vie nocturne"],"prix_base":800},
    {"flag":"🇸🇪","nom":"Stockholm","pays":"Suède","iata":"ARN","booking_id":"Stockholm","tags":["Design","Nature","Culture"],"prix_base":1300},
    {"flag":"🇩🇰","nom":"Copenhague","pays":"Danemark","iata":"CPH","booking_id":"Copenhagen","tags":["Design","Gastronomie","Vélo"],"prix_base":1400},
    {"flag":"🇮🇸","nom":"Reykjavik","pays":"Islande","iata":"KEF","booking_id":"Reykjavik","tags":["Aurores","Volcans","Nature"],"prix_base":2100},
    {"flag":"🇵🇱","nom":"Cracovie","pays":"Pologne","iata":"KRK","booking_id":"Krakow","tags":["Histoire","Culture","Abordable"],"prix_base":450},
    {"flag":"🇹🇷","nom":"Istanbul","pays":"Turquie","iata":"IST","booking_id":"Istanbul","tags":["Culture","Gastronomie","Bosphore"],"prix_base":700},
    {"flag":"🇹🇷","nom":"Cappadoce","pays":"Turquie","iata":"ASR","booking_id":"Cappadocia","tags":["Montgolfière","Paysages","Unique"],"prix_base":800},
    {"flag":"🇬🇧","nom":"Londres","pays":"Royaume-Uni","iata":"LHR","booking_id":"London","tags":["Culture","Histoire","Shopping"],"prix_base":1400},
    {"flag":"🇯🇵","nom":"Tokyo","pays":"Japon","iata":"TYO","booking_id":"Tokyo","tags":["Culture","Gastronomie","Modernité"],"prix_base":2200},
    {"flag":"🇯🇵","nom":"Kyoto","pays":"Japon","iata":"ITM","booking_id":"Kyoto","tags":["Temples","Geishas","Tradition"],"prix_base":1900},
    {"flag":"🇯🇵","nom":"Osaka","pays":"Japon","iata":"KIX","booking_id":"Osaka","tags":["Gastronomie","Vivant","Shopping"],"prix_base":1800},
    {"flag":"🇹🇭","nom":"Bangkok","pays":"Thaïlande","iata":"BKK","booking_id":"Bangkok","tags":["Temples","Street food","Vivant"],"prix_base":900},
    {"flag":"🇹🇭","nom":"Chiang Mai","pays":"Thaïlande","iata":"CNX","booking_id":"Chiang Mai","tags":["Temples","Nature","Détente"],"prix_base":950},
    {"flag":"🇹🇭","nom":"Phuket","pays":"Thaïlande","iata":"HKT","booking_id":"Phuket","tags":["Plage","Fête","Mer"],"prix_base":1100},
    {"flag":"🇻🇳","nom":"Hanoï","pays":"Vietnam","iata":"HAN","booking_id":"Hanoi","tags":["Rue","Histoire","Gastronomie"],"prix_base":700},
    {"flag":"🇻🇳","nom":"Ho Chi Minh","pays":"Vietnam","iata":"SGN","booking_id":"Ho Chi Minh City","tags":["Énergie","Histoire","Street food"],"prix_base":750},
    {"flag":"🇻🇳","nom":"Hội An","pays":"Vietnam","iata":"DAD","booking_id":"Hoi An","tags":["Lanternes","Histoire","Charme"],"prix_base":650},
    {"flag":"🇰🇭","nom":"Siem Reap","pays":"Cambodge","iata":"REP","booking_id":"Siem Reap","tags":["Angkor","Histoire","Culture"],"prix_base":600},
    {"flag":"🇱🇦","nom":"Luang Prabang","pays":"Laos","iata":"LPQ","booking_id":"Luang Prabang","tags":["Temples","Nature","Sérénité"],"prix_base":550},
    {"flag":"🇲🇾","nom":"Kuala Lumpur","pays":"Malaisie","iata":"KUL","booking_id":"Kuala Lumpur","tags":["Tours","Shopping","Gastronomie"],"prix_base":850},
    {"flag":"🇸🇬","nom":"Singapour","pays":"Singapour","iata":"SIN","booking_id":"Singapore","tags":["Modernité","Gastronomie","Propre"],"prix_base":2000},
    {"flag":"🇮🇩","nom":"Bali","pays":"Indonésie","iata":"DPS","booking_id":"Bali","tags":["Spiritualité","Plage","Jungle"],"prix_base":1000},
    {"flag":"🇮🇩","nom":"Lombok","pays":"Indonésie","iata":"LOP","booking_id":"Lombok","tags":["Plage","Volcan","Nature"],"prix_base":900},
    {"flag":"🇵🇭","nom":"Palawan","pays":"Philippines","iata":"PPS","booking_id":"El Nido","tags":["Plage","Lagon","Plongée"],"prix_base":1100},
    {"flag":"🇮🇳","nom":"Goa","pays":"Inde","iata":"GOI","booking_id":"Goa","tags":["Plage","Fête","Détente"],"prix_base":800},
    {"flag":"🇮🇳","nom":"Jaipur","pays":"Inde","iata":"JAI","booking_id":"Jaipur","tags":["Palais","Désert","Couleurs"],"prix_base":700},
    {"flag":"🇳🇵","nom":"Katmandou","pays":"Népal","iata":"KTM","booking_id":"Kathmandu","tags":["Himalaya","Trek","Spirituel"],"prix_base":700},
    {"flag":"🇲🇻","nom":"Malé","pays":"Maldives","iata":"MLE","booking_id":"Male","tags":["Luxe","Plage","Snorkeling"],"prix_base":4500},
    {"flag":"🇨🇳","nom":"Pékin","pays":"Chine","iata":"PEK","booking_id":"Beijing","tags":["Grande Muraille","Histoire","Culture"],"prix_base":1200},
    {"flag":"🇰🇷","nom":"Séoul","pays":"Corée du Sud","iata":"ICN","booking_id":"Seoul","tags":["K-pop","Gastronomie","Modernité"],"prix_base":1200},
    {"flag":"🇦🇪","nom":"Dubaï","pays":"ÉAU","iata":"DXB","booking_id":"Dubai","tags":["Luxe","Gratte-ciel","Shopping"],"prix_base":2200},
    {"flag":"🇯🇴","nom":"Pétra","pays":"Jordanie","iata":"AMM","booking_id":"Petra","tags":["Rochers","Histoire","Désert"],"prix_base":1200},
    {"flag":"🇬🇪","nom":"Tbilissi","pays":"Géorgie","iata":"TBS","booking_id":"Tbilisi","tags":["Vin","Histoire","Caucase"],"prix_base":700},
    {"flag":"🇺🇸","nom":"New York","pays":"États-Unis","iata":"JFK","booking_id":"New York City","tags":["Ville","Shopping","Culture"],"prix_base":2500},
    {"flag":"🇺🇸","nom":"Los Angeles","pays":"États-Unis","iata":"LAX","booking_id":"Los Angeles","tags":["Hollywood","Plage","Culture"],"prix_base":2300},
    {"flag":"🇺🇸","nom":"Miami","pays":"États-Unis","iata":"MIA","booking_id":"Miami","tags":["Plage","Fête","Art Déco"],"prix_base":2200},
    {"flag":"🇺🇸","nom":"Las Vegas","pays":"États-Unis","iata":"LAS","booking_id":"Las Vegas","tags":["Casinos","Shows","Désert"],"prix_base":2000},
    {"flag":"🇨🇦","nom":"Montréal","pays":"Canada","iata":"YUL","booking_id":"Montreal","tags":["French","Culture","Gastronomie"],"prix_base":1600},
    {"flag":"🇲🇽","nom":"Mexico","pays":"Mexique","iata":"MEX","booking_id":"Mexico City","tags":["Culture","Gastronomie","Histoire"],"prix_base":1100},
    {"flag":"🇲🇽","nom":"Cancún","pays":"Mexique","iata":"CUN","booking_id":"Cancun","tags":["Plage","Cenotes","Fête"],"prix_base":1500},
    {"flag":"🇨🇺","nom":"La Havane","pays":"Cuba","iata":"HAV","booking_id":"Havana","tags":["Vintage","Musique","Rhum"],"prix_base":1200},
    {"flag":"🇨🇴","nom":"Carthagène","pays":"Colombie","iata":"CTG","booking_id":"Cartagena","tags":["Colonial","Mer","Couleurs"],"prix_base":1100},
    {"flag":"🇨🇴","nom":"Medellín","pays":"Colombie","iata":"MDE","booking_id":"Medellin","tags":["Printemps","Culture","Énergie"],"prix_base":1000},
    {"flag":"🇵🇪","nom":"Cusco","pays":"Pérou","iata":"LIM","booking_id":"Cusco","tags":["Machu Picchu","Histoire","Inca"],"prix_base":1400},
    {"flag":"🇵🇪","nom":"Lima","pays":"Pérou","iata":"LIM","booking_id":"Lima","tags":["Gastronomie","Mer","Culture"],"prix_base":1200},
    {"flag":"🇧🇷","nom":"Rio de Janeiro","pays":"Brésil","iata":"GIG","booking_id":"Rio de Janeiro","tags":["Carnaval","Plage","Nature"],"prix_base":1500},
    {"flag":"🇦🇷","nom":"Buenos Aires","pays":"Argentine","iata":"EZE","booking_id":"Buenos Aires","tags":["Tango","Gastronomie","Passion"],"prix_base":1000},
    {"flag":"🇦🇷","nom":"Patagonie","pays":"Argentine","iata":"USH","booking_id":"Ushuaia","tags":["Bout du monde","Trek","Nature"],"prix_base":2200},
    {"flag":"🇨🇱","nom":"Santiago","pays":"Chili","iata":"SCL","booking_id":"Santiago","tags":["Vin","Modernité","Culture"],"prix_base":1400},
    {"flag":"🇲🇦","nom":"Marrakech","pays":"Maroc","iata":"RAK","booking_id":"Marrakech","tags":["Souk","Désert","Culture"],"prix_base":700},
    {"flag":"🇲🇦","nom":"Fès","pays":"Maroc","iata":"FEZ","booking_id":"Fez","tags":["Médina","Histoire","Artisanat"],"prix_base":600},
    {"flag":"🇪🇬","nom":"Le Caire","pays":"Égypte","iata":"CAI","booking_id":"Cairo","tags":["Pyramides","Histoire","Culture"],"prix_base":800},
    {"flag":"🇹🇿","nom":"Zanzibar","pays":"Tanzanie","iata":"ZNZ","booking_id":"Zanzibar","tags":["Plage","Épices","Plongée"],"prix_base":1500},
    {"flag":"🇹🇿","nom":"Serengeti","pays":"Tanzanie","iata":"JRO","booking_id":"Serengeti","tags":["Safari","Grande Migration","Nature"],"prix_base":3500},
    {"flag":"🇰🇪","nom":"Nairobi","pays":"Kenya","iata":"NBO","booking_id":"Nairobi","tags":["Safari","Nature","Savane"],"prix_base":2000},
    {"flag":"🇿🇦","nom":"Le Cap","pays":"Afrique du Sud","iata":"CPT","booking_id":"Cape Town","tags":["Vignobles","Montagne","Mer"],"prix_base":1500},
    {"flag":"🇿🇼","nom":"Victoria Falls","pays":"Zimbabwe","iata":"VFA","booking_id":"Victoria Falls","tags":["Chutes","Aventure","Nature"],"prix_base":2200},
    {"flag":"🇸🇨","nom":"Mahé","pays":"Seychelles","iata":"SEZ","booking_id":"Mahe","tags":["Luxe","Plage","Nature"],"prix_base":4000},
    {"flag":"🇲🇺","nom":"Île Maurice","pays":"Maurice","iata":"MRU","booking_id":"Mauritius","tags":["Plage","Luxe","Lagon"],"prix_base":2500},
    {"flag":"🇨🇻","nom":"Cap-Vert","pays":"Cap-Vert","iata":"SID","booking_id":"Sal","tags":["Plage","Musique","Authenticité"],"prix_base":1200},
    {"flag":"🇸🇳","nom":"Dakar","pays":"Sénégal","iata":"DSS","booking_id":"Dakar","tags":["Culture","Musique","Océan"],"prix_base":1000},
    {"flag":"🇦🇺","nom":"Sydney","pays":"Australie","iata":"SYD","booking_id":"Sydney","tags":["Opéra","Plage","Culture"],"prix_base":3000},
    {"flag":"🇦🇺","nom":"Melbourne","pays":"Australie","iata":"MEL","booking_id":"Melbourne","tags":["Art","Gastronomie","Sport"],"prix_base":2800},
    {"flag":"🇳🇿","nom":"Queenstown","pays":"Nv-Zélande","iata":"ZQN","booking_id":"Queenstown","tags":["Aventure","Paysages","Bungee"],"prix_base":3200},
    {"flag":"🇫🇯","nom":"Fidji","pays":"Fidji","iata":"NAN","booking_id":"Fiji","tags":["Plage","Lagon","Luxe"],"prix_base":3500},
    {"flag":"🇵🇫","nom":"Bora Bora","pays":"Polynésie Fr.","iata":"BOB","booking_id":"Bora Bora","tags":["Luxe","Lagon","Romance"],"prix_base":5000},
]

# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────
def prix_total(prix_base, adultes, enfants, bebes):
    return round(prix_base * adultes + prix_base * 0.70 * enfants + prix_base * 0.10 * bebes)

def build_skyscanner_url(orig, dest, d1, d2, adultes, enfants, bebes):
    fmt = lambda d: d.replace("-", "")
    return (
        f"https://www.skyscanner.fr/transport/vols/{orig.lower()}/{dest.lower()}/{fmt(d1)}/{fmt(d2)}/"
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
        f"&group_adults={adultes}&group_children={enfants}&no_rooms=1{aid_param}"
    )

@st.cache_data(ttl=300, show_spinner=False)
def get_skyscanner_prices(orig_iata, dest_iata, d1, d2, adultes):
    if not SKYSCANNER_API_KEY: return None
    url = f"https://{SKYSCANNER_HOST}/api/v1/flights/searchFlights"
    headers = {"X-RapidAPI-Key": SKYSCANNER_API_KEY, "X-RapidAPI-Host": SKYSCANNER_HOST}
    params = {
        "originSkyId": orig_iata, "destinationSkyId": dest_iata,
        "originEntityId": orig_iata, "destinationEntityId": dest_iata,
        "date": d1, "returnDate": d2, "adults": adultes,
        "currency": "EUR", "locale": "fr-FR", "market": "FR", "countryCode": "FR", "cabinClass": "economy",
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        itineraries = resp.json().get("data", {}).get("itineraries", {}).get("results", [])
        if itineraries:
            prices = [it["price"]["raw"] for it in itineraries if it.get("price", {}).get("raw")]
            if prices: return {"price": round(min(prices))}
    except Exception: pass
    return None

@st.cache_data(ttl=300, show_spinner=False)
def get_booking_hotel_price(destination, d1, d2, adultes, nuits):
    if not BOOKING_API_KEY: return None
    headers = {"X-RapidAPI-Key": BOOKING_API_KEY, "X-RapidAPI-Host": BOOKING_HOST}
    try:
        r1 = requests.get(f"https://{BOOKING_HOST}/api/v1/hotels/searchDestination",
                          headers=headers, params={"query": destination}, timeout=6)
        r1.raise_for_status()
        results = r1.json().get("data", [])
        if not results: return None
        dest_id, dest_type = results[0]["dest_id"], results[0]["dest_type"]
        r2 = requests.get(f"https://{BOOKING_HOST}/api/v1/hotels/searchHotels", headers=headers,
                          params={"dest_id": dest_id, "search_type": dest_type,
                                  "arrival_date": d1, "departure_date": d2,
                                  "adults": adultes, "room_qty": 1,
                                  "currency_code": "EUR", "languagecode": "fr", "sort_by": "popularity"}, timeout=8)
        r2.raise_for_status()
        hotels = r2.json().get("data", {}).get("hotels", [])
        if hotels:
            prices = [h["property"]["priceBreakdown"]["grossPrice"]["value"]
                      for h in hotels[:10]
                      if h.get("property", {}).get("priceBreakdown", {}).get("grossPrice", {}).get("value")]
            if prices: return {"price_per_night": round(sum(prices) / len(prices) / nuits)}
    except Exception: pass
    return None

def render_card(r, T, depart_iata, d1_str, d2_str, adultes, nuits, total_v):
    photo_url  = DEST_PHOTOS.get(r["nom"], "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80")
    fav_ribbon = f'<div class="dest-fav-ribbon">★ {T["fav_label"]}</div>' if r["is_favorite"] else ""
    tags_html  = "".join(f'<span class="dest-tag">{t}</span>' for t in r["tags"])
    live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
    live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits)
    price_label = T["price_live"] if live_vol else T["price_est"]
    price_val   = f"{live_vol['price']:,} €" if live_vol else f"{r['prix_estime']:,} €"
    hotel_line  = f'<div class="dest-hotel">{T["hotel_live"].format(p=live_hotel["price_per_night"])}</div>' if live_hotel else ""
    per_pax     = T["per_pax"].format(v=total_v)
    reste_txt   = T["reste"].format(r=r["reste"], n=r["nuits"])
    return f"""
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
</div>"""

# ─────────────────────────────────────────────
#  MÉTÉO
# ─────────────────────────────────────────────
WX_CODES = {
    0:("Ciel dégagé","☀️"), 1:("Principalement clair","🌤"), 2:("Partiellement nuageux","⛅"),
    3:("Couvert","☁️"), 45:("Brouillard","🌫"), 51:("Bruine légère","🌦"),
    61:("Pluie légère","🌧"), 63:("Pluie modérée","🌧"), 71:("Neige légère","🌨"),
    80:("Averses légères","🌦"), 95:("Orage","⛈"),
}

@st.cache_data(ttl=600, show_spinner=False)
def get_weather(city: str):
    try:
        geo = requests.get("https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "PouchVoyage/1.0"}, timeout=6).json()
        if not geo: return None
        lat  = float(geo[0]["lat"]); lon = float(geo[0]["lon"])
        name = geo[0].get("display_name", city).split(",")[0]
        wx = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": lat, "longitude": lon,
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
            "daily": "sunrise,sunset,temperature_2m_max,temperature_2m_min",
            "timezone": "auto", "forecast_days": 1}, timeout=6).json()
        cur = wx.get("current", {}); daily = wx.get("daily", {})
        code = cur.get("weather_code", 0)
        desc, emoji = WX_CODES.get(code, ("—", "🌡"))
        fmt_time = lambda s: s.split("T")[1][:5] if "T" in s else s
        return {
            "city": name, "temp": round(cur.get("temperature_2m", 0)),
            "feels": round(cur.get("apparent_temperature", 0)),
            "humidity": cur.get("relative_humidity_2m", 0),
            "wind": round(cur.get("wind_speed_10m", 0)),
            "desc": desc, "emoji": emoji,
            "temp_max": round(daily.get("temperature_2m_max", [0])[0]),
            "temp_min": round(daily.get("temperature_2m_min", [0])[0]),
            "sunrise": fmt_time(daily.get("sunrise", [""])[0]),
            "sunset":  fmt_time(daily.get("sunset", [""])[0]),
        }
    except Exception: return None

# ─────────────────────────────────────────────
#  COÛT DE LA VIE
# ─────────────────────────────────────────────
COST_DB = {
    "bangkok":{"repas":12,"transport":4,"logement":25,"loisirs":10},
    "chiang mai":{"repas":10,"transport":3,"logement":20,"loisirs":8},
    "bali":{"repas":14,"transport":5,"logement":35,"loisirs":12},
    "tokyo":{"repas":28,"transport":10,"logement":80,"loisirs":20},
    "kyoto":{"repas":25,"transport":8,"logement":70,"loisirs":18},
    "osaka":{"repas":22,"transport":8,"logement":65,"loisirs":16},
    "séoul":{"repas":18,"transport":5,"logement":55,"loisirs":15},
    "seoul":{"repas":18,"transport":5,"logement":55,"loisirs":15},
    "hanoi":{"repas":8,"transport":3,"logement":20,"loisirs":7},
    "hanoï":{"repas":8,"transport":3,"logement":20,"loisirs":7},
    "ho chi minh":{"repas":9,"transport":3,"logement":22,"loisirs":8},
    "singapour":{"repas":22,"transport":8,"logement":90,"loisirs":20},
    "singapore":{"repas":22,"transport":8,"logement":90,"loisirs":20},
    "kuala lumpur":{"repas":12,"transport":4,"logement":30,"loisirs":10},
    "male":{"repas":30,"transport":15,"logement":150,"loisirs":25},
    "malé":{"repas":30,"transport":15,"logement":150,"loisirs":25},
    "kathmandu":{"repas":8,"transport":2,"logement":15,"loisirs":6},
    "phuket":{"repas":15,"transport":6,"logement":40,"loisirs":12},
    "paris":{"repas":35,"transport":10,"logement":100,"loisirs":25},
    "lisbonne":{"repas":22,"transport":6,"logement":60,"loisirs":18},
    "lisbon":{"repas":22,"transport":6,"logement":60,"loisirs":18},
    "barcelone":{"repas":28,"transport":8,"logement":75,"loisirs":20},
    "barcelona":{"repas":28,"transport":8,"logement":75,"loisirs":20},
    "madrid":{"repas":26,"transport":7,"logement":70,"loisirs":18},
    "rome":{"repas":30,"transport":8,"logement":80,"loisirs":20},
    "amsterdam":{"repas":32,"transport":9,"logement":90,"loisirs":22},
    "berlin":{"repas":25,"transport":7,"logement":65,"loisirs":18},
    "prague":{"repas":18,"transport":5,"logement":45,"loisirs":14},
    "budapest":{"repas":16,"transport":4,"logement":40,"loisirs":12},
    "athènes":{"repas":22,"transport":5,"logement":55,"loisirs":15},
    "athens":{"repas":22,"transport":5,"logement":55,"loisirs":15},
    "santorin":{"repas":35,"transport":8,"logement":120,"loisirs":25},
    "santorini":{"repas":35,"transport":8,"logement":120,"loisirs":25},
    "reykjavik":{"repas":50,"transport":15,"logement":120,"loisirs":30},
    "stockholm":{"repas":40,"transport":12,"logement":100,"loisirs":25},
    "copenhague":{"repas":45,"transport":12,"logement":110,"loisirs":28},
    "copenhagen":{"repas":45,"transport":12,"logement":110,"loisirs":28},
    "marrakech":{"repas":14,"transport":4,"logement":35,"loisirs":10},
    "new york":{"repas":45,"transport":12,"logement":150,"loisirs":30},
    "new york city":{"repas":45,"transport":12,"logement":150,"loisirs":30},
    "los angeles":{"repas":40,"transport":15,"logement":130,"loisirs":28},
    "miami":{"repas":38,"transport":14,"logement":120,"loisirs":26},
    "montréal":{"repas":30,"transport":8,"logement":80,"loisirs":20},
    "montreal":{"repas":30,"transport":8,"logement":80,"loisirs":20},
    "buenos aires":{"repas":12,"transport":3,"logement":30,"loisirs":8},
    "rio de janeiro":{"repas":18,"transport":5,"logement":50,"loisirs":12},
    "cusco":{"repas":12,"transport":4,"logement":28,"loisirs":9},
    "nairobi":{"repas":16,"transport":5,"logement":40,"loisirs":10},
    "le cap":{"repas":18,"transport":6,"logement":45,"loisirs":12},
    "cape town":{"repas":18,"transport":6,"logement":45,"loisirs":12},
    "dubaï":{"repas":35,"transport":12,"logement":110,"loisirs":28},
    "dubai":{"repas":35,"transport":12,"logement":110,"loisirs":28},
    "istanbul":{"repas":16,"transport":4,"logement":40,"loisirs":12},
    "tbilissi":{"repas":12,"transport":3,"logement":30,"loisirs":8},
    "sydney":{"repas":40,"transport":10,"logement":110,"loisirs":28},
    "melbourne":{"repas":38,"transport":9,"logement":100,"loisirs":26},
    "queenstown":{"repas":35,"transport":10,"logement":90,"loisirs":22},
    "medellin":{"repas":12,"transport":3,"logement":28,"loisirs":8},
    "bogota":{"repas":13,"transport":3,"logement":30,"loisirs":9},
    "genève":{"repas":55,"transport":15,"logement":130,"loisirs":35},
    "geneva":{"repas":55,"transport":15,"logement":130,"loisirs":35},
    "bruxelles":{"repas":28,"transport":8,"logement":80,"loisirs":20},
}

def get_cost_of_living(city: str):
    key = city.lower().strip()
    if key in COST_DB: return COST_DB[key]
    try:
        url = f"https://www.numbeo.com/api/city_prices?api_key=free&query={urllib.parse.quote(city)}&currency=EUR"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            items = {item["item_id"]: item["average_price"] for item in data.get("prices", [])}
            if items:
                repas     = round((items.get(1, 0) + items.get(2, 0)) / 2)
                transport = round(items.get(20, 0) * 2)
                logement  = round(items.get(26, 0) / 30)
                loisirs   = round(items.get(44, 0) + items.get(28, 0))
                if repas > 0:
                    return {"repas": repas, "transport": transport or 5, "logement": logement or 40, "loisirs": loisirs or 12}
    except Exception: pass
    return None

# ─────────────────────────────────────────────
#  BACKPACKER — données vol inter-régions
# ─────────────────────────────────────────────
VOL_INTER = {
    ("Europe","Europe"):30,     ("Europe","Asie"):450,      ("Europe","Afrique"):300,
    ("Europe","Amériques"):500, ("Europe","Océanie"):900,   ("Europe","Moyen-Orient"):250,
    ("Asie","Asie"):120,        ("Asie","Afrique"):500,     ("Asie","Amériques"):700,
    ("Asie","Océanie"):350,     ("Asie","Moyen-Orient"):200,
    ("Afrique","Afrique"):150,  ("Afrique","Amériques"):700,("Afrique","Océanie"):900,
    ("Amériques","Amériques"):180, ("Amériques","Océanie"):700,
    ("Océanie","Océanie"):200,  ("Moyen-Orient","Moyen-Orient"):150,
}
def cout_vol(r1, r2):
    key = tuple(sorted([r1, r2]))
    return VOL_INTER.get(key, VOL_INTER.get((r1, r2), 400))

REGION_MAP = {
    "Asie du Sud-Est":"Asie",    "Southeast Asia":"Asie",
    "Europe de l'Est":"Europe",  "Eastern Europe":"Europe",
    "Amérique Latine":"Amériques","Latin America":"Amériques",
    "Afrique":"Afrique",          "Africa":"Afrique",
    "Océanie":"Océanie",          "Oceania":"Océanie",
    "Moyen-Orient":"Moyen-Orient","Middle East":"Moyen-Orient",
    "Asia del Sudeste":"Asie",    "Europa del Este":"Europe",
    "América Latina":"Amériques", "África":"Afrique",
    "Oceanía":"Océanie",          "Oriente Medio":"Moyen-Orient",
}
PAYS_REGION = {
    "Japon":"Asie","Thaïlande":"Asie","Vietnam":"Asie","Cambodge":"Asie","Laos":"Asie",
    "Malaisie":"Asie","Singapour":"Asie","Indonésie":"Asie","Philippines":"Asie",
    "Inde":"Asie","Népal":"Asie","Sri Lanka":"Asie","Chine":"Asie","Corée du Sud":"Asie",
    "Géorgie":"Asie","Maldives":"Asie","Myanmar":"Asie",
    "France":"Europe","Espagne":"Europe","Italie":"Europe","Portugal":"Europe",
    "Grèce":"Europe","Croatie":"Europe","République Tchèque":"Europe","Hongrie":"Europe",
    "Autriche":"Europe","Pays-Bas":"Europe","Allemagne":"Europe","Suisse":"Europe",
    "Suède":"Europe","Danemark":"Europe","Norvège":"Europe","Finlande":"Europe",
    "Islande":"Europe","Pologne":"Europe","Roumanie":"Europe","Turquie":"Europe",
    "Royaume-Uni":"Europe","Irlande":"Europe",
    "États-Unis":"Amériques","Canada":"Amériques","Mexique":"Amériques",
    "Costa Rica":"Amériques","Cuba":"Amériques","Panama":"Amériques","Colombie":"Amériques",
    "Pérou":"Amériques","Bolivie":"Amériques","Brésil":"Amériques","Argentine":"Amériques",
    "Chili":"Amériques","Uruguay":"Amériques","Équateur":"Amériques",
    "Maroc":"Afrique","Tunisie":"Afrique","Égypte":"Afrique","Tanzanie":"Afrique",
    "Kenya":"Afrique","Ouganda":"Afrique","Rwanda":"Afrique","Afrique du Sud":"Afrique",
    "Zimbabwe":"Afrique","Botswana":"Afrique","Madagascar":"Afrique","Seychelles":"Afrique",
    "Maurice":"Afrique","Cap-Vert":"Afrique","Sénégal":"Afrique","Éthiopie":"Afrique",
    "Australie":"Océanie","Nv-Zélande":"Océanie","Fidji":"Océanie",
    "Polynésie Fr.":"Océanie","Nv-Calédonie":"Océanie",
    "ÉAU":"Moyen-Orient","Jordanie":"Moyen-Orient","Israël":"Moyen-Orient",
    "Oman":"Moyen-Orient","Qatar":"Moyen-Orient",
}
STYLE_COEF = {
    "Économique 🌿":0.6,"Équilibré ⚖️":1.0,"Confort 🛎":1.6,
    "Budget 🌿":0.6,"Balanced ⚖️":1.0,"Comfort 🛎":1.6,
    "Económico 🌿":0.6,"Equilibrado ⚖️":1.0,
}

DEST_COORDS = {
    "Tokyo":(35.6762,139.6503),"Kyoto":(35.0116,135.7681),"Osaka":(34.6937,135.5022),
    "Bangkok":(13.7563,100.5018),"Chiang Mai":(18.7883,98.9853),"Phuket":(7.8804,98.3923),
    "Hanoï":(21.0285,105.8542),"Ho Chi Minh":(10.8231,106.6297),"Hội An":(15.8801,108.3380),
    "Siem Reap":(13.3633,103.8564),"Luang Prabang":(19.8845,102.1348),
    "Kuala Lumpur":(3.1390,101.6869),"Singapour":(1.3521,103.8198),
    "Bali":(-8.4095,115.1889),"Lombok":(-8.6500,116.3240),"Palawan":(9.8349,118.7384),
    "Goa":(15.2993,74.1240),"Jaipur":(26.9124,75.7873),"Katmandou":(27.7172,85.3240),
    "Malé":(4.1755,73.5093),"Pékin":(39.9042,116.4074),"Séoul":(37.5665,126.9780),
    "Dubaï":(25.2048,55.2708),"Pétra":(30.3285,35.4444),"Tbilissi":(41.6938,44.8015),
    "Lisbonne":(38.7169,-9.1399),"Barcelone":(41.3851,2.1734),"Madrid":(40.4168,-3.7038),
    "Rome":(41.9028,12.4964),"Venise":(45.4408,12.3155),"Florence":(43.7696,11.2558),
    "Nice":(43.7102,7.2620),"Santorin":(36.3932,25.4615),"Athènes":(37.9838,23.7275),
    "Dubrovnik":(42.6507,18.0944),"Prague":(50.0755,14.4378),"Budapest":(47.4979,19.0402),
    "Vienne":(48.2082,16.3738),"Amsterdam":(52.3676,4.9041),"Berlin":(52.5200,13.4050),
    "Stockholm":(59.3293,18.0686),"Copenhague":(55.6761,12.5683),"Reykjavik":(64.1466,-21.9426),
    "Cracovie":(50.0647,19.9450),"Istanbul":(41.0082,28.9784),"Cappadoce":(38.6431,34.8289),
    "Londres":(51.5074,-0.1278),
    "New York":(40.7128,-74.0060),"Los Angeles":(34.0522,-118.2437),"Miami":(25.7617,-80.1918),
    "Las Vegas":(36.1699,-115.1398),"Montréal":(45.5017,-73.5673),
    "Mexico":(19.4326,-99.1332),"Cancún":(21.1619,-86.8515),"La Havane":(23.1136,-82.3666),
    "Carthagène":(10.3910,-75.4794),"Medellín":(6.2442,-75.5812),
    "Cusco":(-13.5319,-71.9675),"Lima":(-12.0464,-77.0428),
    "Rio de Janeiro":(-22.9068,-43.1729),"Buenos Aires":(-34.6037,-58.3816),
    "Patagonie":(-54.8019,-68.3030),"Santiago":(-33.4489,-70.6693),
    "Marrakech":(31.6295,-7.9811),"Fès":(34.0181,-5.0078),
    "Le Caire":(30.0444,31.2357),"Louxor":(25.6872,32.6396),
    "Zanzibar":(-6.1659,39.2026),"Nairobi":(-1.2921,36.8219),"Le Cap":(-33.9249,18.4241),
    "Victoria Falls":(-17.9243,25.8572),"Mahé":(-4.6191,55.4513),
    "Île Maurice":(-20.3484,57.5522),"Dakar":(14.7167,-17.4677),
    "Sydney":(-33.8688,151.2093),"Melbourne":(-37.8136,144.9631),
    "Queenstown":(-45.0312,168.6626),"Fidji":(-17.7134,178.0650),"Bora Bora":(-16.5004,-151.7415),
}

def build_backpacker_itinerary(budget, nb_days, style, regions_pref):
    coef = STYLE_COEF.get(style, 1.0)
    regions_filter = [REGION_MAP.get(r) for r in regions_pref] if regions_pref else None
    pool = []
    for d in DESTINATIONS:
        region = PAYS_REGION.get(d["pays"])
        if not region: continue
        if regions_filter and region not in regions_filter: continue
        cost_day = COST_DB.get(d["nom"].lower(), COST_DB.get(d["booking_id"].lower()))
        if not cost_day:
            cost_day = {"repas": 20, "transport": 6, "logement": 40, "loisirs": 12}
        pool.append({**d, "region": region, "cost_day": cost_day})
    if not pool: return None
    import random
    # Seed stable basé sur les paramètres — stable à l'affichage, varie selon les choix
    _seed = (budget * 7 + nb_days * 13 + len(style) * 31 + len(regions_pref) * 17) % 9999
    random.seed(_seed)
    random.shuffle(pool)
    n_dest = max(2, min(8, nb_days // 5))

    # Sélectionner en diversifiant les régions ET les pays
    chosen, seen_pays, seen_regions = [], set(), {}
    # D'abord un par région (max 2 par région)
    for d in pool:
        reg = d["region"]
        if seen_regions.get(reg, 0) < 2 and d["pays"] not in seen_pays:
            chosen.append(d)
            seen_pays.add(d["pays"])
            seen_regions[reg] = seen_regions.get(reg, 0) + 1
        if len(chosen) >= n_dest: break
    # Compléter si besoin
    if len(chosen) < n_dest:
        for d in pool:
            if d["pays"] not in seen_pays:
                chosen.append(d)
                seen_pays.add(d["pays"])
            if len(chosen) >= n_dest: break
    if len(chosen) < 2:
        chosen = pool[:n_dest]
    days_each = nb_days // len(chosen)
    extra     = nb_days % len(chosen)
    itinerary = []
    total_cost = 0
    prev_region = "Europe"
    for idx, dest in enumerate(chosen):
        nuits  = days_each + (1 if idx < extra else 0)
        cd     = dest["cost_day"]
        vol    = round(cout_vol(prev_region, dest["region"]) * coef)
        hotel  = round(cd["logement"] * coef)
        life   = round((cd["repas"] + cd["transport"] + cd["loisirs"]) * coef)
        subtot = vol + (hotel + life) * nuits
        total_cost += subtot
        prev_region = dest["region"]
        itinerary.append({"dest": dest, "nuits": nuits, "vol": vol, "hotel": hotel, "life": life, "subtot": subtot})
    # ── Vol retour : dernière destination → ville de départ ──
    last_region  = itinerary[-1]["dest"]["region"]
    # Région de départ : on se base sur la ville de départ de l'utilisateur (Europe par défaut)
    return_vol   = round(cout_vol(last_region, "Europe") * coef)
    total_cost  += return_vol
    return itinerary, total_cost, return_vol

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    lang_key = st.selectbox("", list(LANGS.keys()), label_visibility="collapsed")
    st.markdown(f'<div class="powered">{LANGS[lang_key]["powered"]}</div>', unsafe_allow_html=True)

T = LANGS[lang_key]

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-title">Pouch Voyage</div>
  <div class="hero-sub">{T["subtitle"]}</div>
</div>
""", unsafe_allow_html=True)

if "last_action" not in st.session_state:
    st.session_state.last_action = None

# ─────────────────────────────────────────────
#  BARRE DE RECHERCHE HORIZONTALE
# ─────────────────────────────────────────────
with st.container():
    st.markdown("""<div style="background:var(--white);border:1px solid var(--border);padding:1.2rem 1.4rem 0.8rem;margin-bottom:1.5rem;">""", unsafe_allow_html=True)
    row1 = st.columns([2, 1.5, 1.5, 1, 1, 1, 1.2])
    with row1[0]:
        ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
        ville_idx = st.selectbox(T["depart"], range(len(ville_options)), format_func=lambda i: ville_options[i])
        depart_iata = VILLES_DEPART[ville_idx]["iata"]
        depart_nom  = VILLES_DEPART[ville_idx]["nom"]
        depart_flag = VILLES_DEPART[ville_idx]["flag"]
    with row1[1]:
        d1 = st.date_input(T["dates"] + " ↗", value=date.today() + timedelta(days=30), min_value=date.today())
    with row1[2]:
        d2 = st.date_input(T["dates"] + " ↙", value=date.today() + timedelta(days=37), min_value=date.today())
    with row1[3]:
        adultes = st.number_input(T["adultes"], min_value=1, max_value=9, value=2, step=1)
    with row1[4]:
        enfants = st.number_input(T["enfants"], min_value=0, max_value=9, value=0, step=1)
    with row1[5]:
        bebes   = st.number_input(T["bebes"],   min_value=0, max_value=9, value=0, step=1)
    with row1[6]:
        budget  = st.number_input(T["budget"], min_value=500, max_value=50000, value=3000, step=100)

    row2 = st.columns([4, 1, 1])
    with row2[0]:
        st.markdown(f'<div style="font-size:0.72rem;letter-spacing:0.06em;text-transform:uppercase;color:#6B6560;margin-bottom:3px">{T["fav"]}</div>', unsafe_allow_html=True)
        fav = st.text_input("fav_h", placeholder=T["fav_ph"], label_visibility="collapsed")
    with row2[2]:
        st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)
        if st.button(T["search"], key="btn_search", use_container_width=True, type="primary"):
            st.session_state.last_action = "search"
    chercher = st.session_state.last_action == "search"
    st.markdown("</div>", unsafe_allow_html=True)

tab_search, tab_cost, tab_weather, tab_bpack = st.tabs([T["tab_search"], T["tab_cost"], T["tab_weather"], T["tab_bpack"]])

# ══════════════════════════════════════════════
#  ONGLET 1 — RECHERCHE
# ══════════════════════════════════════════════
with tab_search:
    chercher = st.session_state.get("last_action") == "search"
    if not chercher:
        # ── Mur de photos d'accueil — 2 colonnes élégantes ──
        HERO_DESTINATIONS = [
            ("Tokyo",          "🇯🇵", "Japon",         "Culture & modernité"),
            ("Bali",           "🇮🇩", "Indonésie",     "Spiritualité & jungle"),
            ("Santorin",       "🇬🇷", "Grèce",         "Romance & mer Égée"),
            ("Marrakech",      "🇲🇦", "Maroc",         "Souk & désert"),
            ("Rio de Janeiro", "🇧🇷", "Brésil",        "Carnaval & plage"),
            ("Reykjavik",      "🇮🇸", "Islande",       "Aurores & volcans"),
        ]
        cols = st.columns(2)
        for idx, (nom, flag, pays, tagline) in enumerate(HERO_DESTINATIONS):
            photo = DEST_PHOTOS.get(nom, "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80")
            with cols[idx % 2]:
                st.markdown(f"""
<div class="dest-card" style="cursor:default;margin-bottom:1.4rem;">
  <div class="photo-wrap">
    <img class="dest-photo hero-photo" src="{photo}" alt="{nom}" loading="lazy">
  </div>
  <div class="dest-body" style="padding:1rem 1.4rem 0.9rem;">
    <div class="dest-name">{flag} {nom}</div>
    <div class="dest-country">{pays}</div>
    <div style="font-size:0.75rem;color:var(--muted);font-style:italic;margin-top:2px;">{tagline}</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:center;font-size:0.78rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--muted);margin-top:0.5rem;">{T["fill_form"]}</div>', unsafe_allow_html=True)

    elif (d2 - d1).days <= 0:
        st.markdown(f'<div class="msg-sage">⟶ {T["date_err"]}</div>', unsafe_allow_html=True)
    else:
        nuits     = (d2 - d1).days
        d1_str    = d1.strftime("%Y-%m-%d")
        d2_str    = d2.strftime("%Y-%m-%d")
        fav_lower = fav.lower().strip()
        total_v   = adultes + enfants + bebes
        resultats = []
        for dest in DESTINATIONS:
            prix_est = prix_total(dest["prix_base"], adultes, enfants, bebes)
            if prix_est > budget: continue
            score = 2 if prix_est <= budget * 0.75 else 0
            nom_lower = dest["nom"].lower() + " " + dest["pays"].lower()
            if fav_lower and (fav_lower in nom_lower or any(m in fav_lower for m in nom_lower.split())):
                score += 10
            resultats.append({
                **dest, "prix_estime": prix_est, "nuits": nuits,
                "reste": budget - prix_est, "score": score, "is_favorite": score >= 10,
                "url_sky":  build_skyscanner_url(depart_iata, dest["iata"], d1_str, d2_str, adultes, enfants, bebes),
                "url_book": build_booking_url(dest["booking_id"], d1_str, d2_str, adultes, enfants),
            })
        # Trier par score favori d'abord, puis diversifier par région
        import random as _random
        import hashlib as _hashlib
        # Seed basé sur les paramètres pour avoir de la variété mais de la reproductibilité
        _seed = int(_hashlib.md5(f"{depart_iata}{d1_str}{budget}{adultes}".encode()).hexdigest(), 16) % 10000
        _random.seed(_seed)

        # Séparer favoris et autres
        favoris  = [r for r in resultats if r["is_favorite"]]
        autres   = [r for r in resultats if not r["is_favorite"]]

        # Regrouper les autres par région et prendre 1-2 par région pour diversifier
        regions_vues = {}
        for r in autres:
            reg = PAYS_REGION.get(r["pays"], "Autre")
            regions_vues.setdefault(reg, []).append(r)

        # Mélanger l'ordre dans chaque région
        for reg in regions_vues:
            _random.shuffle(regions_vues[reg])

        # Construire une liste équilibrée : 1 par région en round-robin
        diversifies = []
        max_par_region = 3
        for _ in range(max_par_region):
            for reg, dests in regions_vues.items():
                if dests:
                    diversifies.append(dests.pop(0))

        # Mélanger légèrement pour éviter le même ordre à chaque fois
        _random.shuffle(diversifies)

        resultats = favoris + diversifies
        resultats = resultats[:12]
        st.markdown(f"""
<div class="summary">
  <b>{len(resultats)}</b> destination(s)
  <span class="summary-dot">·</span> <b>{nuits}</b> nuit(s)
  <span class="summary-dot">·</span> <b>{total_v}</b> voyageur(s)
  <span class="summary-dot">·</span> <b>{budget:,} €</b>
</div>""", unsafe_allow_html=True)
        if not resultats:
            st.markdown(f'<div class="no-result">{T["no_result"]}</div>', unsafe_allow_html=True)
        else:
            cols = st.columns(3)
            for i, r in enumerate(resultats):
                with cols[i % 3]:
                    html = render_card(r, T, depart_iata, d1_str, d2_str, adultes, nuits, total_v)
                    st.markdown(html, unsafe_allow_html=True)
                    b1, b2 = st.columns(2)
                    with b1: st.link_button(T["btn_sky"],  r["url_sky"],  use_container_width=True)
                    with b2: st.link_button(T["btn_book"], r["url_book"], use_container_width=True)
                    st.markdown("<div style='margin-bottom:1.2rem'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ONGLET 2 — COÛT DE LA VIE
# ══════════════════════════════════════════════
with tab_cost:
    st.markdown(f"""
<div class="hero" style="padding:1.2rem 0 1.8rem; margin-bottom:1.5rem;">
  <div class="hero-title" style="font-size:2.2rem;">{T["cost_title"]}</div>
  <div class="hero-sub">{T["cost_sub"]}</div>
</div>""", unsafe_allow_html=True)
    col_inp, col_days, col_btn = st.columns([3, 1, 1])
    with col_inp:
        city_input = st.text_input(T["cost_input"], placeholder=T["cost_ph"], label_visibility="collapsed")
    with col_days:
        nb_days = st.number_input(T["cost_ndays"], min_value=1, max_value=365, value=7, step=1, label_visibility="collapsed")
    with col_btn:
        calc_btn = st.button(T["cost_btn"], use_container_width=True)
    if calc_btn and city_input.strip():
        cost = get_cost_of_living(city_input.strip())
        if not cost:
            st.markdown(f'<div class="msg-sage">⟶ {T["cost_err"]}</div>', unsafe_allow_html=True)
        else:
            cats   = T["cost_cats"]
            total  = sum(cost.values())
            icons  = {"repas":"🍽","transport":"🚌","logement":"🏨","loisirs":"🎭"}
            colors = {"repas":"#C9A96E","transport":"#8BA888","logement":"#7B9CB8","loisirs":"#B8847B"}
            st.markdown(f"""
<div class="dest-card" style="max-width:520px;margin:0 auto 2rem;">
  <div class="dest-body">
    <div class="dest-name" style="font-size:2rem;">{city_input.strip().title()}</div>
    <div class="dest-country" style="margin-bottom:1.2rem;">{T["cost_src"]}</div>
    <div style="display:flex;flex-direction:column;gap:10px;margin-bottom:1.4rem;">""", unsafe_allow_html=True)
            for key, label in cats.items():
                val = cost[key]; pct = round(val / total * 100)
                st.markdown(f"""
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:28px;text-align:center;font-size:1rem;">{icons[key]}</div>
        <div style="flex:1;">
          <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
            <span style="font-size:0.72rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted)">{label}</span>
            <span style="font-family:'Cormorant Garamond',serif;font-size:1rem;color:var(--ink)">{val} €</span>
          </div>
          <div style="height:3px;background:var(--border);">
            <div style="height:3px;width:{pct}%;background:{colors[key]};"></div>
          </div>
        </div>
      </div>""", unsafe_allow_html=True)
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
</div>""", unsafe_allow_html=True)
    elif calc_btn:
        st.markdown('<div class="msg-sage">⟶ Entrez le nom d\'une ville.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="no-result">Tapez une ville ci-dessus et cliquez sur Calculer.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ONGLET 3 — MÉTÉO
# ══════════════════════════════════════════════
with tab_weather:
    st.markdown(f"""
<div class="hero" style="padding:1.2rem 0 1.8rem; margin-bottom:1.5rem;">
  <div class="hero-title" style="font-size:2.2rem;">{T["wx_title"]}</div>
  <div class="hero-sub">{T["wx_sub"]}</div>
</div>""", unsafe_allow_html=True)
    col_wx, col_wxbtn = st.columns([4, 1])
    with col_wx:
        wx_city = st.text_input(T["wx_input"], placeholder=T["wx_ph"], label_visibility="collapsed")
    with col_wxbtn:
        wx_btn = st.button(T["wx_btn"], use_container_width=True)
    if wx_btn and wx_city.strip():
        wx = get_weather(wx_city.strip())
        if not wx:
            st.markdown(f'<div class="msg-sage">⟶ {T["wx_err"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            border-bottom:1px solid var(--border);padding-bottom:1rem;margin-bottom:1.2rem;">
  <div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:400;color:var(--ink);line-height:1;">{wx["city"]}</div>
    <div style="font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--muted);margin-top:4px;">{wx["desc"]}</div>
  </div>
  <div style="font-size:3.5rem;line-height:1;">{wx["emoji"]}</div>
</div>""", unsafe_allow_html=True)
            col_t, col_mm = st.columns([2, 1])
            with col_t:
                st.markdown(f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:5rem;font-weight:300;color:var(--ink);line-height:1;margin-bottom:4px;">{wx["temp"]}°C</div>', unsafe_allow_html=True)
            with col_mm:
                st.markdown(f'<div style="padding-top:1.2rem;"><div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">Max · Min</div><div style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:var(--ink);">{wx["temp_max"]}° · {wx["temp_min"]}°</div></div>', unsafe_allow_html=True)
            st.markdown("<div style='height:1px;background:var(--border);margin:1rem 0'></div>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric(T["wx_feels"],   f"{wx['feels']}°C")
            c2.metric(T["wx_humidity"],f"{wx['humidity']} %")
            c3.metric(T["wx_wind"],    f"{wx['wind']} km/h")
            c4.metric(f"{T['wx_sunrise']} · {T['wx_sunset']}", f"{wx['sunrise']} · {wx['sunset']}")
            st.markdown(f'<div style="font-size:0.65rem;letter-spacing:0.07em;color:var(--muted);text-align:center;margin-top:1.2rem;">{T["wx_src"]}</div>', unsafe_allow_html=True)
    elif wx_btn:
        st.markdown(f'<div class="msg-sage">⟶ {T["wx_err"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="no-result">{T["wx_prompt"]}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ONGLET 4 — BACKPACKER
# ══════════════════════════════════════════════
with tab_bpack:
    st.markdown(f"""
<div class="hero" style="padding:1.2rem 0 1.8rem; margin-bottom:1.5rem;">
  <div class="hero-title" style="font-size:2.2rem;">{T["bp_title"]}</div>
  <div class="hero-sub">{T["bp_sub"]}</div>
</div>""", unsafe_allow_html=True)

    col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
    with col_b1: bp_budget = st.slider(T["bp_budget"], 500, 15000, 4000, 100)
    with col_b2: bp_days   = st.number_input(T["bp_days"], min_value=7, max_value=365, value=30, step=1)
    with col_b3: bp_style  = st.selectbox(T["bp_style"], T["bp_styles"])

    # ── Sélection par continent ──
    CONTINENTS = [
        {"key": "Europe",       "label": "Europe",       "emoji": "🏛"},
        {"key": "Asie",         "label": "Asie",         "emoji": "🏯"},
        {"key": "Amériques",    "label": "Amériques",    "emoji": "🗽"},
        {"key": "Afrique",      "label": "Afrique",      "emoji": "🦁"},
        {"key": "Océanie",      "label": "Océanie",      "emoji": "🦘"},
        {"key": "Moyen-Orient", "label": "Moyen-Orient", "emoji": "🕌"},
    ]
    if "bp_continents" not in st.session_state:
        st.session_state.bp_continents = set()

    st.markdown(
        "<div style='font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;"
        "color:var(--muted);margin:1rem 0 0.4rem;'>Continents &mdash; tous si aucun sélectionné</div>",
        unsafe_allow_html=True
    )
    cont_cols = st.columns(6)
    for ci, cont in enumerate(CONTINENTS):
        with cont_cols[ci]:
            is_on = cont["key"] in st.session_state.bp_continents
            lbl   = ("✓ " if is_on else "") + cont["emoji"] + " " + cont["label"]
            if st.button(lbl, key=f"cont_{cont['key']}", use_container_width=True):
                if is_on:
                    st.session_state.bp_continents.discard(cont["key"])
                else:
                    st.session_state.bp_continents.add(cont["key"])
                st.rerun()

    if st.session_state.bp_continents:
        badges = "".join([
            f"<span style='background:var(--ink);color:var(--cream);font-size:0.68rem;"
            f"letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;margin-right:6px;'>{c['emoji']} {c['label']}</span>"
            for c in CONTINENTS if c["key"] in st.session_state.bp_continents
        ])
        st.markdown(f"<div style='margin:0.3rem 0 0.6rem;'>{badges}</div>", unsafe_allow_html=True)
        bp_regions = list(st.session_state.bp_continents)
    else:
        bp_regions = []

    if st.button(T["bp_btn"], key="btn_bpack", use_container_width=True):
        st.session_state.last_action = "bpack"
    bp_btn = st.session_state.last_action == "bpack"

    try:
        d1_str = d1.strftime("%Y-%m-%d")
        d2_str = d2.strftime("%Y-%m-%d")
    except Exception:
        d1_str = (date.today() + timedelta(days=30)).strftime("%Y-%m-%d")
        d2_str = (date.today() + timedelta(days=60)).strftime("%Y-%m-%d")

    if bp_btn:
        result = build_backpacker_itinerary(bp_budget, bp_days, bp_style, bp_regions)
        if not result:
            st.markdown(f'<div class="msg-sage">⟶ {T["bp_warning"]}</div>', unsafe_allow_html=True)
        else:
            itinerary, total_cost, return_vol = result
            over_budget = total_cost > bp_budget

            st.markdown(f"""
<div class="summary">
  <b>{len(itinerary)}</b> pays &nbsp;·&nbsp;
  <b>{bp_days}</b> jours &nbsp;·&nbsp;
  <b style="color:{'#B85555' if over_budget else '#4A6E4E'};">{total_cost:,} €</b>
  {'⚠ dépasse votre budget' if over_budget else '✓ dans votre budget'}
</div>""", unsafe_allow_html=True)

            st.markdown("""
<div style="position:relative;margin-bottom:2rem;overflow:hidden;">
  <img src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1400&q=85"
       style="width:100%;height:220px;object-fit:cover;display:block;filter:brightness(0.72);">
  <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
    <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;
                color:#FEFCF8;letter-spacing:0.12em;text-shadow:0 2px 12px rgba(0,0,0,0.4);">
      Votre itinéraire
    </div>
  </div>
</div>""", unsafe_allow_html=True)

            # ── Étapes ──
            for idx, step in enumerate(itinerary):
                dest = step["dest"]
                st.markdown(f"""
<div style="background:var(--white);border:1px solid var(--border);
            display:flex;align-items:center;justify-content:space-between;
            padding:1rem 1.4rem;margin-bottom:8px;gap:1rem;">
  <div style="display:flex;align-items:center;gap:14px;flex:2;">
    <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;color:var(--border);font-weight:300;min-width:32px;text-align:center;">{idx+1:02d}</div>
    <div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:var(--ink);line-height:1;">{dest["flag"]} {dest["nom"]}</div>
      <div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);margin-top:2px;">{dest["pays"]} · {step["nuits"]} nuits</div>
    </div>
  </div>
  <div style="display:flex;gap:2rem;flex:3;justify-content:center;">
    <div style="text-align:center;">
      <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">✈ Vol</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--ink);">{step["vol"]:,} €</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">🏨 /nuit</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--ink);">{step["hotel"]:,} €</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">🍽 /jour</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--ink);">{step["life"]:,} €</div>
    </div>
  </div>
  <div style="text-align:right;flex:1;">
    <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">Total</div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--ink);font-weight:400;">{step["subtot"]:,} €</div>
  </div>
</div>""", unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                with b1: st.link_button(f"✈ {T['btn_sky']} — {dest['nom']}", build_skyscanner_url(depart_iata, dest["iata"], d1_str, d2_str, 1, 0, 0), use_container_width=True)
                with b2: st.link_button(f"⌂ {T['btn_book']} — {dest['nom']}", build_booking_url(dest["booking_id"], d1_str, d2_str, 1, 0), use_container_width=True)
                st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)

            # ── VOL RETOUR — ligne distincte avec bordure dorée ──
            last_dest = itinerary[-1]["dest"]
            st.markdown(f"""
<div class="return-flight-row">
  <div style="display:flex;align-items:center;gap:14px;flex:2;">
    <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;color:var(--gold);font-weight:300;min-width:32px;text-align:center;">↩</div>
    <div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;color:var(--ink);line-height:1;">
        {last_dest["flag"]} {last_dest["nom"]} → {depart_flag} {depart_nom}
      </div>
      <div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);margin-top:2px;">
        {T["bp_return_label"]} · {T["bp_return_est"]}
      </div>
    </div>
  </div>
  <div style="display:flex;gap:2rem;flex:3;justify-content:center;">
    <div style="text-align:center;">
      <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">✈ Vol retour</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--ink);">{return_vol:,} €</div>
    </div>
  </div>
  <div style="text-align:right;flex:1;">
    <div style="font-size:0.62rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">Inclus dans total</div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--gold);font-weight:400;">{return_vol:,} €</div>
  </div>
</div>""", unsafe_allow_html=True)
            # Bouton Skyscanner vol retour
            ret_url = build_skyscanner_url(last_dest["iata"], depart_iata, d1_str, d2_str, 1, 0, 0)
            st.link_button(f"✈ Réserver le vol retour → {depart_nom}", ret_url, use_container_width=False)
            st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

            # ── Récap budget total ──
            pct = min(100, round(total_cost / bp_budget * 100))
            st.markdown(f"""
<div class="dest-card" style="margin-top:1.5rem;">
  <div class="dest-body">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.8rem;">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;">{T["bp_grand"]}</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:var(--ink);">
        {total_cost:,} € <span style="font-size:1rem;color:var(--muted);">/ {bp_budget:,} €</span>
      </div>
    </div>
    <div style="height:4px;background:var(--border);margin-bottom:0.6rem;">
      <div style="height:4px;width:{pct}%;background:{'#B85555' if over_budget else '#7A9E7E'};"></div>
    </div>
    <div style="font-size:0.65rem;letter-spacing:0.07em;color:var(--muted);text-align:center;">{T["bp_src"]}</div>
  </div>
</div>""", unsafe_allow_html=True)

            # ── Carte interactive ──
            st.markdown("---")
            st.markdown(f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.4rem;color:var(--ink);margin-bottom:0.8rem;">Carte de l\'itinéraire</div>', unsafe_allow_html=True)
            try:
                import folium
                from streamlit_folium import st_folium
                first_coords = DEST_COORDS.get(itinerary[0]["dest"]["nom"], (20, 10))
                m = folium.Map(location=first_coords, zoom_start=2, tiles="CartoDB positron")
                coords_list = []
                for step_idx, step in enumerate(itinerary):
                    coords = DEST_COORDS.get(step["dest"]["nom"])
                    if not coords: continue
                    coords_list.append(coords)
                    folium.Marker(
                        location=coords,
                        popup=folium.Popup(f"<b>{step['dest']['flag']} {step['dest']['nom']}</b><br>{step['dest']['pays']}<br>{step['nuits']} nuits<br>~{step['subtot']:,} €", max_width=200),
                        tooltip=f"{step_idx+1}. {step['dest']['nom']}",
                        icon=folium.DivIcon(
                            html=f'<div style="background:#0D0D0D;color:#F5F0E8;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:500;font-family:Inter,sans-serif;box-shadow:0 2px 6px rgba(0,0,0,0.3);">{step_idx+1}</div>',
                            icon_size=(28, 28), icon_anchor=(14, 14))
                    ).add_to(m)
                # Ajouter le point de départ/retour
                depart_coords_map = next(
                    (v for v in [DEST_COORDS.get(depart_nom)] if v), None
                )
                if depart_coords_map and coords_list:
                    # Ligne retour : dernière dest → départ
                    folium.PolyLine(
                        [coords_list[-1], depart_coords_map],
                        color="#C9A96E", weight=2, opacity=0.8, dash_array="4 6"
                    ).add_to(m)
                    folium.Marker(
                        location=depart_coords_map,
                        tooltip=f"↩ {depart_nom} (retour)",
                        icon=folium.DivIcon(
                            html=f'<div style="background:#C9A96E;color:#0D0D0D;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,0.3);">↩</div>',
                            icon_size=(28, 28), icon_anchor=(14, 14))
                    ).add_to(m)
                if len(coords_list) > 1:
                    folium.PolyLine(coords_list, color="#C9A96E", weight=2, opacity=0.7, dash_array="6 4").add_to(m)
                st_folium(m, use_container_width=True, height=420)
            except ImportError:
                st.markdown('<div class="msg-sage">⟶ Installez folium et streamlit-folium : <code>pip install folium streamlit-folium</code></div>', unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="no-result">{T["bp_prompt"]}</div>', unsafe_allow_html=True)
