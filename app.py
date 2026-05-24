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

  /* messages — vert sauge */
  .msg-sage {
    background: #EEF2EE;
    border-left: 2px solid #7A9E7E;
    color: #4A6E4E;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    padding: 0.7rem 1rem;
    margin: 0.5rem 0;
    font-style: italic;
  }

  /* no result */
  .no-result { text-align:center; padding:5rem 2rem; color:var(--muted); font-size:0.9rem; font-weight:300; letter-spacing:0.05em; }

  /* info / error / success — tout en vert sauge */
  div[data-testid="stAlert"] {
    background: #EEF2EE !important;
    border: 1px solid #7A9E7E !important;
    border-radius: 0 !important;
    color: #4A6E4E !important;
    font-size: 0.82rem !important;
  }
  div[data-testid="stAlert"] svg { color: #7A9E7E !important; fill: #7A9E7E !important; }
  div[data-testid="stAlert"] p { color: #4A6E4E !important; }

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
        "btn_book":   "⌂  Booking",
        "fav_label":  "Favori",
        "per_pax":    "pour {v} voyageur(s)",
        "tab_weather":    "☁  Météo",
        "tab_bpack":     "🎒  Backpacker",
        "wx_title":       "Météo par destination",
        "wx_sub":         "Entrez une ville pour connaître la météo actuelle",
        "wx_input":       "Ville",
        "wx_ph":          "ex : Tokyo, Lisbonne, Dubaï…",
        "wx_btn":         "Voir la météo",
        "wx_feels":       "Ressenti",
        "wx_humidity":    "Humidité",
        "wx_wind":        "Vent",
        "wx_sunrise":     "Lever",
        "wx_sunset":      "Coucher",
        "wx_err":         "Ville introuvable. Vérifiez l'orthographe.",
        "wx_prompt":      "Tapez une ville et cliquez sur Voir la météo.",
        "wx_src":         "Source : Open-Meteo + OpenStreetMap (données temps réel)",
        "bp_title":      "Itinéraire Backpacker",
        "bp_sub":        "Entrez votre budget total et vos préférences — on construit votre tour du monde",
        "bp_budget":     "Budget total (€)",
        "bp_days":       "Nombre de jours",
        "bp_style":      "Style de voyage",
        "bp_styles":     ["Économique 🌿", "Équilibré ⚖️", "Confort 🛎"],
        "bp_region":     "Régions préférées (optionnel)",
        "bp_regions":    ["Asie du Sud-Est", "Europe de l'Est", "Amérique Latine", "Afrique", "Océanie", "Moyen-Orient"],
        "bp_btn":        "Générer l'itinéraire",
        "bp_prompt":     "Remplissez les champs et générez votre itinéraire.",
        "bp_day_label":  "Jour {d}",
        "bp_flight":     "Vol estimé",
        "bp_hotel":      "Hébergement/nuit",
        "bp_life":       "Vie quotidienne",
        "bp_total_dest": "Total destination",
        "bp_grand":      "Total itinéraire",
        "bp_nights":     "{n} nuits",
        "bp_warning":    "Budget insuffisant pour un itinéraire multi-pays. Augmentez le budget ou réduisez les jours.",
        "bp_src":        "Estimations basées sur données Numbeo & prix moyens compagnies aériennes",
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
        "btn_book":   "⌂  Booking",
        "fav_label":  "Favourite",
        "per_pax":    "for {v} traveller(s)",
        "tab_weather":    "☁  Weather",
        "tab_bpack":     "🎒  Backpacker",
        "wx_title":       "Weather by destination",
        "wx_sub":         "Enter a city to check current weather",
        "wx_input":       "City",
        "wx_ph":          "e.g. Tokyo, Lisbon, Dubai…",
        "wx_btn":         "Check weather",
        "wx_feels":       "Feels like",
        "wx_humidity":    "Humidity",
        "wx_wind":        "Wind",
        "wx_sunrise":     "Sunrise",
        "wx_sunset":      "Sunset",
        "wx_err":         "City not found. Check spelling.",
        "wx_prompt":      "Enter a city and click Check weather.",
        "wx_src":         "Source: Open-Meteo + OpenStreetMap (live data)",
        "bp_title":      "Backpacker Itinerary",
        "bp_sub":        "Enter your total budget and preferences — we'll build your world trip",
        "bp_budget":     "Total budget (€)",
        "bp_days":       "Number of days",
        "bp_style":      "Travel style",
        "bp_styles":     ["Budget 🌿", "Balanced ⚖️", "Comfort 🛎"],
        "bp_regions":    ["Southeast Asia", "Eastern Europe", "Latin America", "Africa", "Oceania", "Middle East"],
        "bp_region":     "Preferred regions (optional)",
        "bp_btn":        "Generate itinerary",
        "bp_prompt":     "Fill in the fields and generate your itinerary.",
        "bp_day_label":  "Day {d}",
        "bp_flight":     "Est. flight",
        "bp_hotel":      "Accommodation/night",
        "bp_life":       "Daily living",
        "bp_total_dest": "Total per destination",
        "bp_grand":      "Total itinerary",
        "bp_nights":     "{n} nights",
        "bp_warning":    "Budget too low for a multi-country itinerary. Increase budget or reduce days.",
        "bp_src":        "Estimates based on Numbeo data & average airline prices",
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
        "btn_book":   "⌂  Booking",
        "fav_label":  "Favorito",
        "per_pax":    "para {v} viajero(s)",
        "tab_weather":    "☁  Tiempo",
        "tab_bpack":     "🎒  Backpacker",
        "wx_title":       "Tiempo por destino",
        "wx_sub":         "Introduce una ciudad para ver el tiempo actual",
        "wx_input":       "Ciudad",
        "wx_ph":          "ej: Tokio, Lisboa, Dubái…",
        "wx_btn":         "Ver el tiempo",
        "wx_feels":       "Sensación",
        "wx_humidity":    "Humedad",
        "wx_wind":        "Viento",
        "wx_sunrise":     "Amanecer",
        "wx_sunset":      "Atardecer",
        "wx_err":         "Ciudad no encontrada. Verifica la ortografía.",
        "wx_prompt":      "Introduce una ciudad y haz clic en Ver el tiempo.",
        "wx_src":         "Fuente: Open-Meteo + OpenStreetMap (datos en tiempo real)",
        "bp_title":      "Itinerario Mochilero",
        "bp_sub":        "Introduce tu presupuesto total y preferencias — construimos tu viaje al mundo",
        "bp_budget":     "Presupuesto total (€)",
        "bp_days":       "Número de días",
        "bp_style":      "Estilo de viaje",
        "bp_styles":     ["Económico 🌿", "Equilibrado ⚖️", "Confort 🛎"],
        "bp_regions":    ["Asia del Sudeste", "Europa del Este", "América Latina", "África", "Oceanía", "Oriente Medio"],
        "bp_region":     "Regiones preferidas (opcional)",
        "bp_btn":        "Generar itinerario",
        "bp_prompt":     "Rellena los campos y genera tu itinerario.",
        "bp_day_label":  "Día {d}",
        "bp_flight":     "Vuelo estimado",
        "bp_hotel":      "Alojamiento/noche",
        "bp_life":       "Vida diaria",
        "bp_total_dest": "Total por destino",
        "bp_grand":      "Total itinerario",
        "bp_nights":     "{n} noches",
        "bp_warning":    "Presupuesto insuficiente. Aumenta el presupuesto o reduce los días.",
        "bp_src":        "Estimaciones basadas en datos de Numbeo y precios medios de aerolíneas",
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
    # ── EUROPE ──
    {"flag":"🇵🇹","nom":"Lisbonne",       "pays":"Portugal",        "iata":"LIS","booking_id":"Lisbon",          "tags":["Histoire","Fado","Gastronomie"],      "prix_base":700},
    {"flag":"🇪🇸","nom":"Barcelone",      "pays":"Espagne",         "iata":"BCN","booking_id":"Barcelona",       "tags":["Architecture","Plage","Vie nocturne"],"prix_base":900},
    {"flag":"🇪🇸","nom":"Madrid",         "pays":"Espagne",         "iata":"MAD","booking_id":"Madrid",          "tags":["Musées","Gastronomie","Culture"],      "prix_base":850},
    {"flag":"🇮🇹","nom":"Rome",           "pays":"Italie",          "iata":"FCO","booking_id":"Rome",            "tags":["Histoire","Art","Gastronomie"],        "prix_base":950},
    {"flag":"🇮🇹","nom":"Venise",         "pays":"Italie",          "iata":"VCE","booking_id":"Venice",          "tags":["Romance","Architecture","Art"],        "prix_base":1100},
    {"flag":"🇮🇹","nom":"Florence",       "pays":"Italie",          "iata":"FLR","booking_id":"Florence",        "tags":["Art","Renaissance","Gastronomie"],     "prix_base":900},
    {"flag":"🇫🇷","nom":"Nice",           "pays":"France",          "iata":"NCE","booking_id":"Nice",            "tags":["Plage","Côte d'Azur","Gastronomie"],   "prix_base":1000},
    {"flag":"🇬🇷","nom":"Santorin",       "pays":"Grèce",           "iata":"JTR","booking_id":"Santorini",       "tags":["Romance","Mer","Gastronomie"],         "prix_base":1600},
    {"flag":"🇬🇷","nom":"Athènes",        "pays":"Grèce",           "iata":"ATH","booking_id":"Athens",          "tags":["Histoire","Mythologie","Culture"],     "prix_base":750},
    {"flag":"🇬🇷","nom":"Crète",          "pays":"Grèce",           "iata":"HER","booking_id":"Crete",           "tags":["Plage","Histoire","Nature"],           "prix_base":800},
    {"flag":"🇭🇷","nom":"Dubrovnik",      "pays":"Croatie",         "iata":"DBV","booking_id":"Dubrovnik",       "tags":["Mer","Histoire","Beauté"],             "prix_base":1000},
    {"flag":"🇭🇷","nom":"Split",          "pays":"Croatie",         "iata":"SPU","booking_id":"Split",           "tags":["Mer","Histoire","Animé"],              "prix_base":850},
    {"flag":"🇨🇿","nom":"Prague",         "pays":"République Tchèque","iata":"PRG","booking_id":"Prague",        "tags":["Architecture","Bière","Histoire"],     "prix_base":600},
    {"flag":"🇭🇺","nom":"Budapest",       "pays":"Hongrie",         "iata":"BUD","booking_id":"Budapest",        "tags":["Thermes","Architecture","Nuit"],       "prix_base":550},
    {"flag":"🇦🇹","nom":"Vienne",         "pays":"Autriche",        "iata":"VIE","booking_id":"Vienna",          "tags":["Musique","Musées","Architecture"],     "prix_base":900},
    {"flag":"🇳🇱","nom":"Amsterdam",      "pays":"Pays-Bas",        "iata":"AMS","booking_id":"Amsterdam",       "tags":["Canaux","Musées","Vélo"],              "prix_base":1100},
    {"flag":"🇩🇪","nom":"Berlin",         "pays":"Allemagne",       "iata":"BER","booking_id":"Berlin",          "tags":["Histoire","Art","Vie nocturne"],       "prix_base":800},
    {"flag":"🇩🇪","nom":"Munich",         "pays":"Allemagne",       "iata":"MUC","booking_id":"Munich",          "tags":["Bière","Culture","Nature"],            "prix_base":950},
    {"flag":"🇨🇭","nom":"Zurich",         "pays":"Suisse",          "iata":"ZRH","booking_id":"Zurich",          "tags":["Luxe","Nature","Finance"],             "prix_base":1800},
    {"flag":"🇨🇭","nom":"Interlaken",     "pays":"Suisse",          "iata":"ZRH","booking_id":"Interlaken",      "tags":["Alpes","Aventure","Nature"],           "prix_base":1600},
    {"flag":"🇸🇪","nom":"Stockholm",      "pays":"Suède",           "iata":"ARN","booking_id":"Stockholm",       "tags":["Design","Nature","Culture"],           "prix_base":1300},
    {"flag":"🇩🇰","nom":"Copenhague",     "pays":"Danemark",        "iata":"CPH","booking_id":"Copenhagen",      "tags":["Design","Gastronomie","Vélo"],         "prix_base":1400},
    {"flag":"🇳🇴","nom":"Oslo",           "pays":"Norvège",         "iata":"OSL","booking_id":"Oslo",            "tags":["Fjords","Nature","Design"],            "prix_base":1600},
    {"flag":"🇳🇴","nom":"Bergen",         "pays":"Norvège",         "iata":"BGO","booking_id":"Bergen",          "tags":["Fjords","Nature","Paysages"],          "prix_base":1400},
    {"flag":"🇫🇮","nom":"Helsinki",       "pays":"Finlande",        "iata":"HEL","booking_id":"Helsinki",        "tags":["Design","Sauna","Nature"],             "prix_base":1200},
    {"flag":"🇮🇸","nom":"Reykjavik",      "pays":"Islande",         "iata":"KEF","booking_id":"Reykjavik",       "tags":["Aurores","Volcans","Nature"],          "prix_base":2100},
    {"flag":"🇵🇱","nom":"Cracovie",       "pays":"Pologne",         "iata":"KRK","booking_id":"Krakow",          "tags":["Histoire","Culture","Abordable"],      "prix_base":450},
    {"flag":"🇷🇴","nom":"Bucarest",       "pays":"Roumanie",        "iata":"OTP","booking_id":"Bucharest",       "tags":["Histoire","Vie nocturne","Abordable"],  "prix_base":400},
    {"flag":"🇷🇴","nom":"Brasov",         "pays":"Roumanie",        "iata":"OTP","booking_id":"Brasov",          "tags":["Château","Montagne","Médiéval"],       "prix_base":380},
    {"flag":"🇧🇬","nom":"Sofia",          "pays":"Bulgarie",        "iata":"SOF","booking_id":"Sofia",           "tags":["Histoire","Monastères","Abordable"],   "prix_base":380},
    {"flag":"🇷🇸","nom":"Belgrade",       "pays":"Serbie",          "iata":"BEG","booking_id":"Belgrade",        "tags":["Vie nocturne","Gastronomie","Abordable"],"prix_base":380},
    {"flag":"🇲🇪","nom":"Kotor",          "pays":"Monténégro",      "iata":"TGD","booking_id":"Kotor",           "tags":["Mer","Médiéval","Paysages"],           "prix_base":600},
    {"flag":"🇦🇱","nom":"Tirana",         "pays":"Albanie",         "iata":"TIA","booking_id":"Tirana",          "tags":["Découverte","Abordable","Authentique"], "prix_base":350},
    {"flag":"🇲🇹","nom":"La Valette",     "pays":"Malte",           "iata":"MLA","booking_id":"Valletta",        "tags":["Histoire","Mer","Plongée"],            "prix_base":750},
    {"flag":"🇨🇾","nom":"Chypre",         "pays":"Chypre",          "iata":"LCA","booking_id":"Larnaca",         "tags":["Plage","Histoire","Mer"],              "prix_base":700},
    {"flag":"🇹🇷","nom":"Istanbul",       "pays":"Turquie",         "iata":"IST","booking_id":"Istanbul",        "tags":["Culture","Gastronomie","Bosphore"],    "prix_base":700},
    {"flag":"🇹🇷","nom":"Cappadoce",      "pays":"Turquie",         "iata":"ASR","booking_id":"Cappadocia",      "tags":["Montgolfière","Paysages","Unique"],    "prix_base":800},
    {"flag":"🇹🇷","nom":"Antalya",        "pays":"Turquie",         "iata":"AYT","booking_id":"Antalya",         "tags":["Plage","Histoire","Mer"],              "prix_base":650},
    {"flag":"🇬🇧","nom":"Londres",        "pays":"Royaume-Uni",     "iata":"LHR","booking_id":"London",          "tags":["Culture","Histoire","Shopping"],       "prix_base":1400},
    {"flag":"🇬🇧","nom":"Édimbourg",      "pays":"Royaume-Uni",     "iata":"EDI","booking_id":"Edinburgh",       "tags":["Châteaux","Whisky","Histoire"],        "prix_base":1100},
    {"flag":"🇮🇪","nom":"Dublin",         "pays":"Irlande",         "iata":"DUB","booking_id":"Dublin",          "tags":["Pub","Culture","Vert"],                "prix_base":1200},
    # ── ASIE ──
    {"flag":"🇯🇵","nom":"Tokyo",          "pays":"Japon",           "iata":"TYO","booking_id":"Tokyo",           "tags":["Culture","Gastronomie","Modernité"],   "prix_base":2200},
    {"flag":"🇯🇵","nom":"Kyoto",          "pays":"Japon",           "iata":"ITM","booking_id":"Kyoto",           "tags":["Temples","Geishas","Tradition"],       "prix_base":1900},
    {"flag":"🇯🇵","nom":"Osaka",          "pays":"Japon",           "iata":"KIX","booking_id":"Osaka",           "tags":["Gastronomie","Vivant","Shopping"],     "prix_base":1800},
    {"flag":"🇹🇭","nom":"Bangkok",        "pays":"Thaïlande",       "iata":"BKK","booking_id":"Bangkok",         "tags":["Temples","Street food","Vivant"],      "prix_base":900},
    {"flag":"🇹🇭","nom":"Chiang Mai",     "pays":"Thaïlande",       "iata":"CNX","booking_id":"Chiang Mai",      "tags":["Temples","Nature","Détente"],          "prix_base":950},
    {"flag":"🇹🇭","nom":"Phuket",         "pays":"Thaïlande",       "iata":"HKT","booking_id":"Phuket",          "tags":["Plage","Fête","Mer"],                  "prix_base":1100},
    {"flag":"🇹🇭","nom":"Koh Samui",      "pays":"Thaïlande",       "iata":"USM","booking_id":"Koh Samui",       "tags":["Île","Plage","Détente"],               "prix_base":1200},
    {"flag":"🇻🇳","nom":"Hanoï",          "pays":"Vietnam",         "iata":"HAN","booking_id":"Hanoi",           "tags":["Rue","Histoire","Gastronomie"],        "prix_base":700},
    {"flag":"🇻🇳","nom":"Ho Chi Minh",    "pays":"Vietnam",         "iata":"SGN","booking_id":"Ho Chi Minh City","tags":["Énergie","Histoire","Street food"],    "prix_base":750},
    {"flag":"🇻🇳","nom":"Da Nang",        "pays":"Vietnam",         "iata":"DAD","booking_id":"Da Nang",         "tags":["Plage","Pont","Détente"],              "prix_base":700},
    {"flag":"🇻🇳","nom":"Hội An",         "pays":"Vietnam",         "iata":"DAD","booking_id":"Hoi An",          "tags":["Lanternes","Histoire","Charme"],       "prix_base":650},
    {"flag":"🇰🇭","nom":"Siem Reap",      "pays":"Cambodge",        "iata":"REP","booking_id":"Siem Reap",       "tags":["Angkor","Histoire","Culture"],         "prix_base":600},
    {"flag":"🇲🇲","nom":"Bagan",          "pays":"Myanmar",         "iata":"NYU","booking_id":"Bagan",           "tags":["Temples","Montgolfière","Unique"],     "prix_base":700},
    {"flag":"🇱🇦","nom":"Luang Prabang",  "pays":"Laos",            "iata":"LPQ","booking_id":"Luang Prabang",   "tags":["Temples","Nature","Sérénité"],         "prix_base":550},
    {"flag":"🇲🇾","nom":"Kuala Lumpur",   "pays":"Malaisie",        "iata":"KUL","booking_id":"Kuala Lumpur",    "tags":["Tours","Shopping","Gastronomie"],      "prix_base":850},
    {"flag":"🇲🇾","nom":"Penang",         "pays":"Malaisie",        "iata":"PEN","booking_id":"Penang",          "tags":["Street art","Gastronomie","Histoire"], "prix_base":700},
    {"flag":"🇸🇬","nom":"Singapour",      "pays":"Singapour",       "iata":"SIN","booking_id":"Singapore",       "tags":["Modernité","Gastronomie","Propre"],    "prix_base":2000},
    {"flag":"🇮🇩","nom":"Bali",           "pays":"Indonésie",       "iata":"DPS","booking_id":"Bali",            "tags":["Spiritualité","Plage","Jungle"],       "prix_base":1000},
    {"flag":"🇮🇩","nom":"Lombok",         "pays":"Indonésie",       "iata":"LOP","booking_id":"Lombok",          "tags":["Plage","Volcan","Nature"],             "prix_base":900},
    {"flag":"🇮🇩","nom":"Yogyakarta",     "pays":"Indonésie",       "iata":"JOG","booking_id":"Yogyakarta",      "tags":["Borobudur","Culture","Art"],           "prix_base":700},
    {"flag":"🇵🇭","nom":"Palawan",        "pays":"Philippines",     "iata":"PPS","booking_id":"El Nido",         "tags":["Plage","Lagon","Plongée"],             "prix_base":1100},
    {"flag":"🇵🇭","nom":"Cebu",           "pays":"Philippines",     "iata":"CEB","booking_id":"Cebu City",       "tags":["Plongée","Plage","Baleines"],          "prix_base":900},
    {"flag":"🇮🇳","nom":"Goa",            "pays":"Inde",            "iata":"GOI","booking_id":"Goa",             "tags":["Plage","Fête","Détente"],              "prix_base":800},
    {"flag":"🇮🇳","nom":"Jaipur",         "pays":"Inde",            "iata":"JAI","booking_id":"Jaipur",          "tags":["Palais","Désert","Couleurs"],          "prix_base":700},
    {"flag":"🇮🇳","nom":"Mumbai",         "pays":"Inde",            "iata":"BOM","booking_id":"Mumbai",          "tags":["Bollywood","Énergie","Contrastes"],    "prix_base":750},
    {"flag":"🇮🇳","nom":"Kerala",         "pays":"Inde",            "iata":"COK","booking_id":"Kochi",           "tags":["Backwaters","Nature","Détente"],       "prix_base":700},
    {"flag":"🇮🇳","nom":"Varanasi",       "pays":"Inde",            "iata":"VNS","booking_id":"Varanasi",        "tags":["Spirituel","Gange","Unique"],          "prix_base":650},
    {"flag":"🇳🇵","nom":"Katmandou",      "pays":"Népal",           "iata":"KTM","booking_id":"Kathmandu",       "tags":["Himalaya","Trek","Spirituel"],         "prix_base":700},
    {"flag":"🇱🇰","nom":"Colombo",        "pays":"Sri Lanka",       "iata":"CMB","booking_id":"Colombo",         "tags":["Temples","Plage","Nature"],            "prix_base":800},
    {"flag":"🇲🇻","nom":"Malé",           "pays":"Maldives",        "iata":"MLE","booking_id":"Male",            "tags":["Luxe","Plage","Snorkeling"],           "prix_base":4500},
    {"flag":"🇨🇳","nom":"Pékin",          "pays":"Chine",           "iata":"PEK","booking_id":"Beijing",         "tags":["Grande Muraille","Histoire","Culture"],"prix_base":1200},
    {"flag":"🇨🇳","nom":"Shanghai",       "pays":"Chine",           "iata":"PVG","booking_id":"Shanghai",        "tags":["Modernité","Finance","Architecture"],  "prix_base":1300},
    {"flag":"🇨🇳","nom":"Guilin",         "pays":"Chine",           "iata":"KWL","booking_id":"Guilin",          "tags":["Paysages","Rizières","Nature"],        "prix_base":1000},
    {"flag":"🇰🇷","nom":"Séoul",          "pays":"Corée du Sud",    "iata":"ICN","booking_id":"Seoul",           "tags":["K-pop","Gastronomie","Modernité"],     "prix_base":1200},
    {"flag":"🇰🇷","nom":"Busan",          "pays":"Corée du Sud",    "iata":"PUS","booking_id":"Busan",           "tags":["Mer","Plage","Gastronomie"],           "prix_base":1100},
    {"flag":"🇹🇼","nom":"Taipei",         "pays":"Taïwan",          "iata":"TPE","booking_id":"Taipei",          "tags":["Street food","Modernité","Nature"],    "prix_base":1100},
    {"flag":"🇲🇳","nom":"Oulan-Bator",    "pays":"Mongolie",        "iata":"ULN","booking_id":"Ulaanbaatar",     "tags":["Steppes","Nomades","Aventure"],        "prix_base":1200},
    {"flag":"🇺🇿","nom":"Samarcande",     "pays":"Ouzbékistan",     "iata":"SKD","booking_id":"Samarkand",       "tags":["Route de la soie","Histoire","Unique"], "prix_base":900},
    {"flag":"🇬🇪","nom":"Tbilissi",       "pays":"Géorgie",         "iata":"TBS","booking_id":"Tbilisi",         "tags":["Vin","Histoire","Caucause"],           "prix_base":700},
    {"flag":"🇦🇲","nom":"Erevan",         "pays":"Arménie",         "iata":"EVN","booking_id":"Yerevan",         "tags":["Histoire","Monastères","Abordable"],   "prix_base":650},
    {"flag":"🇦🇿","nom":"Bakou",          "pays":"Azerbaïdjan",     "iata":"GYD","booking_id":"Baku",            "tags":["Pétrole","Architecture","Unique"],     "prix_base":800},
    {"flag":"🇯🇴","nom":"Pétra",          "pays":"Jordanie",        "iata":"AMM","booking_id":"Petra",           "tags":["Rochers","Histoire","Désert"],         "prix_base":1200},
    {"flag":"🇮🇱","nom":"Tel Aviv",       "pays":"Israël",          "iata":"TLV","booking_id":"Tel Aviv",        "tags":["Plage","Tech","Gastronomie"],          "prix_base":1500},
    {"flag":"🇦🇪","nom":"Dubaï",          "pays":"ÉAU",             "iata":"DXB","booking_id":"Dubai",           "tags":["Luxe","Gratte-ciel","Shopping"],       "prix_base":2200},
    {"flag":"🇦🇪","nom":"Abu Dhabi",      "pays":"ÉAU",             "iata":"AUH","booking_id":"Abu Dhabi",       "tags":["Luxe","Mosquée","Culture"],            "prix_base":2000},
    {"flag":"🇴🇲","nom":"Mascate",        "pays":"Oman",            "iata":"MCT","booking_id":"Muscat",          "tags":["Désert","Authenticité","Nature"],      "prix_base":1300},
    {"flag":"🇶🇦","nom":"Doha",           "pays":"Qatar",           "iata":"DOH","booking_id":"Doha",            "tags":["Architecture","Luxe","Culture"],       "prix_base":1800},
    # ── AMÉRIQUES ──
    {"flag":"🇺🇸","nom":"New York",       "pays":"États-Unis",      "iata":"JFK","booking_id":"New York City",   "tags":["Ville","Shopping","Culture"],          "prix_base":2500},
    {"flag":"🇺🇸","nom":"Los Angeles",    "pays":"États-Unis",      "iata":"LAX","booking_id":"Los Angeles",     "tags":["Hollywood","Plage","Culture"],         "prix_base":2300},
    {"flag":"🇺🇸","nom":"Miami",          "pays":"États-Unis",      "iata":"MIA","booking_id":"Miami",           "tags":["Plage","Fête","Art Déco"],             "prix_base":2200},
    {"flag":"🇺🇸","nom":"San Francisco",  "pays":"États-Unis",      "iata":"SFO","booking_id":"San Francisco",   "tags":["Tech","Pont","Culture"],               "prix_base":2400},
    {"flag":"🇺🇸","nom":"New Orleans",    "pays":"États-Unis",      "iata":"MSY","booking_id":"New Orleans",     "tags":["Jazz","Gastronomie","Fête"],           "prix_base":1900},
    {"flag":"🇺🇸","nom":"Las Vegas",      "pays":"États-Unis",      "iata":"LAS","booking_id":"Las Vegas",       "tags":["Casinos","Shows","Désert"],            "prix_base":2000},
    {"flag":"🇺🇸","nom":"Hawaii",         "pays":"États-Unis",      "iata":"HNL","booking_id":"Honolulu",        "tags":["Plage","Volcan","Nature"],             "prix_base":3000},
    {"flag":"🇨🇦","nom":"Montréal",       "pays":"Canada",          "iata":"YUL","booking_id":"Montreal",        "tags":["French","Culture","Gastronomie"],      "prix_base":1600},
    {"flag":"🇨🇦","nom":"Vancouver",      "pays":"Canada",          "iata":"YVR","booking_id":"Vancouver",       "tags":["Nature","Montagne","Mer"],             "prix_base":1800},
    {"flag":"🇨🇦","nom":"Toronto",        "pays":"Canada",          "iata":"YYZ","booking_id":"Toronto",         "tags":["Multiculturel","Chutes","Modernité"],  "prix_base":1700},
    {"flag":"🇲🇽","nom":"Mexico",         "pays":"Mexique",         "iata":"MEX","booking_id":"Mexico City",     "tags":["Culture","Gastronomie","Histoire"],    "prix_base":1100},
    {"flag":"🇲🇽","nom":"Cancún",         "pays":"Mexique",         "iata":"CUN","booking_id":"Cancun",          "tags":["Plage","Cenotes","Fête"],              "prix_base":1500},
    {"flag":"🇲🇽","nom":"Oaxaca",         "pays":"Mexique",         "iata":"OAX","booking_id":"Oaxaca",          "tags":["Culture","Gastronomie","Art"],         "prix_base":1000},
    {"flag":"🇨🇷","nom":"San José",       "pays":"Costa Rica",      "iata":"SJO","booking_id":"San Jose",        "tags":["Nature","Biodiversité","Surf"],        "prix_base":1400},
    {"flag":"🇨🇺","nom":"La Havane",      "pays":"Cuba",            "iata":"HAV","booking_id":"Havana",          "tags":["Vintage","Musique","Rhum"],            "prix_base":1200},
    {"flag":"🇵🇦","nom":"Panama City",    "pays":"Panama",          "iata":"PTY","booking_id":"Panama City",     "tags":["Canal","Modernité","Jungle"],          "prix_base":1300},
    {"flag":"🇨🇴","nom":"Carthagène",     "pays":"Colombie",        "iata":"CTG","booking_id":"Cartagena",       "tags":["Colonial","Mer","Couleurs"],           "prix_base":1100},
    {"flag":"🇨🇴","nom":"Medellín",       "pays":"Colombie",        "iata":"MDE","booking_id":"Medellin",        "tags":["Printemps","Culture","Énergie"],       "prix_base":1000},
    {"flag":"🇨🇴","nom":"Bogotá",         "pays":"Colombie",        "iata":"BOG","booking_id":"Bogota",          "tags":["Altitude","Gastronomie","Art"],        "prix_base":1100},
    {"flag":"🇵🇪","nom":"Cusco",          "pays":"Pérou",           "iata":"LIM","booking_id":"Cusco",           "tags":["Machu Picchu","Histoire","Inca"],      "prix_base":1400},
    {"flag":"🇵🇪","nom":"Lima",           "pays":"Pérou",           "iata":"LIM","booking_id":"Lima",            "tags":["Gastronomie","Mer","Culture"],         "prix_base":1200},
    {"flag":"🇧🇴","nom":"La Paz",         "pays":"Bolivie",         "iata":"LPB","booking_id":"La Paz",          "tags":["Altitude","Salar","Unique"],           "prix_base":900},
    {"flag":"🇧🇷","nom":"Rio de Janeiro", "pays":"Brésil",          "iata":"GIG","booking_id":"Rio de Janeiro",  "tags":["Carnaval","Plage","Nature"],           "prix_base":1500},
    {"flag":"🇧🇷","nom":"São Paulo",      "pays":"Brésil",          "iata":"GRU","booking_id":"Sao Paulo",       "tags":["Gastronomie","Culture","Énergie"],     "prix_base":1400},
    {"flag":"🇧🇷","nom":"Florianópolis",  "pays":"Brésil",          "iata":"FLN","booking_id":"Florianopolis",   "tags":["Plage","Nature","Surf"],               "prix_base":1200},
    {"flag":"🇦🇷","nom":"Buenos Aires",   "pays":"Argentine",       "iata":"EZE","booking_id":"Buenos Aires",    "tags":["Tango","Gastronomie","Passion"],       "prix_base":1000},
    {"flag":"🇦🇷","nom":"Patagonie",      "pays":"Argentine",       "iata":"USH","booking_id":"Ushuaia",         "tags":["Bout du monde","Trek","Nature"],       "prix_base":2200},
    {"flag":"🇨🇱","nom":"Santiago",       "pays":"Chili",           "iata":"SCL","booking_id":"Santiago",        "tags":["Vin","Modernité","Culture"],           "prix_base":1400},
    {"flag":"🇨🇱","nom":"Atacama",        "pays":"Chili",           "iata":"CJC","booking_id":"San Pedro de Atacama","tags":["Désert","Étoiles","Unique"],      "prix_base":1600},
    {"flag":"🇺🇾","nom":"Montevideo",     "pays":"Uruguay",         "iata":"MVD","booking_id":"Montevideo",      "tags":["Détente","Bord de mer","Culture"],     "prix_base":1100},
    {"flag":"🇪🇨","nom":"Galápagos",      "pays":"Équateur",        "iata":"GPS","booking_id":"Galapagos",       "tags":["Faune","Nature","Unique"],             "prix_base":3000},
    # ── AFRIQUE ──
    {"flag":"🇲🇦","nom":"Marrakech",      "pays":"Maroc",           "iata":"RAK","booking_id":"Marrakech",       "tags":["Souk","Désert","Culture"],             "prix_base":700},
    {"flag":"🇲🇦","nom":"Essaouira",      "pays":"Maroc",           "iata":"ESU","booking_id":"Essaouira",       "tags":["Vent","Médina","Authenticité"],        "prix_base":600},
    {"flag":"🇲🇦","nom":"Fès",            "pays":"Maroc",           "iata":"FEZ","booking_id":"Fez",             "tags":["Médina","Histoire","Artisanat"],       "prix_base":600},
    {"flag":"🇹🇳","nom":"Tunis",          "pays":"Tunisie",         "iata":"TUN","booking_id":"Tunis",           "tags":["Histoire","Médina","Plage"],           "prix_base":500},
    {"flag":"🇪🇬","nom":"Le Caire",       "pays":"Égypte",          "iata":"CAI","booking_id":"Cairo",           "tags":["Pyramides","Histoire","Culture"],      "prix_base":800},
    {"flag":"🇪🇬","nom":"Louxor",         "pays":"Égypte",          "iata":"LXR","booking_id":"Luxor",           "tags":["Pharaons","Temples","Nil"],            "prix_base":700},
    {"flag":"🇸🇸","nom":"Zanzibar",       "pays":"Tanzanie",        "iata":"ZNZ","booking_id":"Zanzibar",        "tags":["Plage","Épices","Plongée"],            "prix_base":1500},
    {"flag":"🇹🇿","nom":"Serengeti",      "pays":"Tanzanie",        "iata":"JRO","booking_id":"Serengeti",       "tags":["Safari","Grande Migration","Nature"],  "prix_base":3500},
    {"flag":"🇰🇪","nom":"Nairobi",        "pays":"Kenya",           "iata":"NBO","booking_id":"Nairobi",         "tags":["Safari","Nature","Savane"],            "prix_base":2000},
    {"flag":"🇺🇬","nom":"Kampala",        "pays":"Ouganda",         "iata":"EBB","booking_id":"Kampala",         "tags":["Gorilles","Nature","Découverte"],      "prix_base":1800},
    {"flag":"🇷🇼","nom":"Kigali",         "pays":"Rwanda",          "iata":"KGL","booking_id":"Kigali",          "tags":["Gorilles","Propre","Nature"],          "prix_base":2000},
    {"flag":"🇿🇦","nom":"Le Cap",         "pays":"Afrique du Sud",  "iata":"CPT","booking_id":"Cape Town",       "tags":["Vignobles","Montagne","Mer"],          "prix_base":1500},
    {"flag":"🇿🇦","nom":"Johannesburg",   "pays":"Afrique du Sud",  "iata":"JNB","booking_id":"Johannesburg",    "tags":["Apartheid","Culture","Safari"],        "prix_base":1400},
    {"flag":"🇿🇼","nom":"Victoria Falls", "pays":"Zimbabwe",        "iata":"VFA","booking_id":"Victoria Falls",  "tags":["Chutes","Aventure","Nature"],          "prix_base":2200},
    {"flag":"🇧🇼","nom":"Botswana",       "pays":"Botswana",        "iata":"GBE","booking_id":"Maun",            "tags":["Delta Okavango","Safari","Luxe"],      "prix_base":3500},
    {"flag":"🇲🇬","nom":"Antananarivo",   "pays":"Madagascar",      "iata":"TNR","booking_id":"Antananarivo",    "tags":["Lémuriens","Nature","Unique"],         "prix_base":1400},
    {"flag":"🇸🇨","nom":"Mahé",           "pays":"Seychelles",      "iata":"SEZ","booking_id":"Mahe",            "tags":["Luxe","Plage","Nature"],               "prix_base":4000},
    {"flag":"🇲🇺","nom":"Île Maurice",    "pays":"Maurice",         "iata":"MRU","booking_id":"Mauritius",       "tags":["Plage","Luxe","Lagon"],               "prix_base":2500},
    {"flag":"🇷🇪","nom":"La Réunion",     "pays":"France",          "iata":"RUN","booking_id":"Saint-Denis",     "tags":["Volcan","Trek","Nature"],              "prix_base":1800},
    {"flag":"🇨🇻","nom":"Cap-Vert",       "pays":"Cap-Vert",        "iata":"SID","booking_id":"Sal",             "tags":["Plage","Musique","Authenticité"],      "prix_base":1200},
    {"flag":"🇸🇳","nom":"Dakar",          "pays":"Sénégal",         "iata":"DSS","booking_id":"Dakar",           "tags":["Culture","Musique","Océan"],           "prix_base":1000},
    {"flag":"🇪🇹","nom":"Addis-Abeba",    "pays":"Éthiopie",        "iata":"ADD","booking_id":"Addis Ababa",     "tags":["Histoire","Café","Découverte"],        "prix_base":1100},
    {"flag":"🇬🇭","nom":"Accra",          "pays":"Ghana",           "iata":"ACC","booking_id":"Accra",           "tags":["Côte","Histoire","Musique"],           "prix_base":1200},
    # ── OCÉANIE ──
    {"flag":"🇦🇺","nom":"Sydney",         "pays":"Australie",       "iata":"SYD","booking_id":"Sydney",          "tags":["Opéra","Plage","Culture"],             "prix_base":3000},
    {"flag":"🇦🇺","nom":"Melbourne",      "pays":"Australie",       "iata":"MEL","booking_id":"Melbourne",       "tags":["Art","Gastronomie","Sport"],           "prix_base":2800},
    {"flag":"🇦🇺","nom":"Cairns",         "pays":"Australie",       "iata":"CNS","booking_id":"Cairns",          "tags":["Grande Barrière","Forêt","Plongée"],   "prix_base":2500},
    {"flag":"🇦🇺","nom":"Uluru",          "pays":"Australie",       "iata":"AYQ","booking_id":"Uluru",           "tags":["Rocher sacré","Désert","Unique"],      "prix_base":2800},
    {"flag":"🇳🇿","nom":"Queenstown",     "pays":"Nv-Zélande",      "iata":"ZQN","booking_id":"Queenstown",      "tags":["Aventure","Paysages","Bungee"],        "prix_base":3200},
    {"flag":"🇳🇿","nom":"Auckland",       "pays":"Nv-Zélande",      "iata":"AKL","booking_id":"Auckland",        "tags":["Harbour","Culture","Nature"],          "prix_base":3000},
    {"flag":"🇫🇯","nom":"Fidji",          "pays":"Fidji",           "iata":"NAN","booking_id":"Fiji",            "tags":["Plage","Lagon","Luxe"],               "prix_base":3500},
    {"flag":"🇵🇫","nom":"Bora Bora",      "pays":"Polynésie Fr.",   "iata":"BOB","booking_id":"Bora Bora",       "tags":["Luxe","Lagon","Romance"],             "prix_base":5000},
    {"flag":"🇳🇨","nom":"Nouméa",         "pays":"Nv-Calédonie",    "iata":"NOU","booking_id":"Noumea",          "tags":["Lagon","Plage","Nature"],             "prix_base":2800},
    {"flag":"🇵🇬","nom":"Port Moresby",   "pays":"Papouasie",       "iata":"POM","booking_id":"Port Moresby",    "tags":["Aventure","Tribaux","Unique"],         "prix_base":2500},
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
#  MÉTÉO — Open-Meteo (gratuit, sans clé API)
# ─────────────────────────────────────────────
WX_CODES = {
    0:  ("Ciel dégagé",       "☀️"),
    1:  ("Principalement clair","🌤"),  2: ("Partiellement nuageux","⛅"),
    3:  ("Couvert",            "☁️"),
    45: ("Brouillard",         "🌫"),  48: ("Brouillard givrant",  "🌫"),
    51: ("Bruine légère",      "🌦"),  53: ("Bruine modérée",      "🌦"),  55: ("Bruine dense","🌧"),
    61: ("Pluie légère",       "🌧"),  63: ("Pluie modérée",       "🌧"),  65: ("Pluie forte","🌧"),
    71: ("Neige légère",       "🌨"),  73: ("Neige modérée",       "🌨"),  75: ("Neige forte","❄️"),
    80: ("Averses légères",    "🌦"),  81: ("Averses modérées",    "🌧"),  82: ("Averses fortes","⛈"),
    95: ("Orage",              "⛈"),  96: ("Orage avec grêle",    "⛈"),  99: ("Orage violent","⛈"),
}

@st.cache_data(ttl=600, show_spinner=False)
def get_weather(city: str) -> dict | None:
    """Géocode la ville via Nominatim puis appelle Open-Meteo."""
    try:
        # Géocodage
        geo = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "PouchVoyage/1.0"},
            timeout=6
        ).json()
        if not geo:
            return None
        lat  = float(geo[0]["lat"])
        lon  = float(geo[0]["lon"])
        name = geo[0].get("display_name", city).split(",")[0]

        # Météo actuelle
        wx = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
                "daily":   "sunrise,sunset,temperature_2m_max,temperature_2m_min",
                "timezone": "auto", "forecast_days": 1,
            },
            timeout=6
        ).json()

        cur   = wx.get("current", {})
        daily = wx.get("daily", {})
        code  = cur.get("weather_code", 0)
        desc, emoji = WX_CODES.get(code, ("—", "🌡"))

        sunrise = daily.get("sunrise", [""])[0]
        sunset  = daily.get("sunset",  [""])[0]
        fmt_time = lambda s: s.split("T")[1][:5] if "T" in s else s

        return {
            "city":       name,
            "temp":       round(cur.get("temperature_2m", 0)),
            "feels":      round(cur.get("apparent_temperature", 0)),
            "humidity":   cur.get("relative_humidity_2m", 0),
            "wind":       round(cur.get("wind_speed_10m", 0)),
            "desc":       desc,
            "emoji":      emoji,
            "is_day":     cur.get("is_day", 1),
            "temp_max":   round(daily.get("temperature_2m_max", [0])[0]),
            "temp_min":   round(daily.get("temperature_2m_min", [0])[0]),
            "sunrise":    fmt_time(sunrise),
            "sunset":     fmt_time(sunset),
        }
    except Exception:
        return None

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

tab_search, tab_cost, tab_weather, tab_bpack = st.tabs([T["tab_search"], T["tab_cost"], T["tab_weather"], T["tab_bpack"]])

# ══════════════════════════════════════════════
#  ONGLET 1 — RECHERCHE DE VOYAGES
# ══════════════════════════════════════════════
with tab_search:
    if not chercher:
        st.markdown(f'<div class="no-result">{T["fill_form"]}</div>', unsafe_allow_html=True)
    elif (d2 - d1).days <= 0:
        st.markdown(f'<div class="msg-sage">⟶ {T["date_err"]}</div>', unsafe_allow_html=True)
    else:
        nuits = (d2 - d1).days
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
            st.markdown(f'<div class="msg-sage">⟶ {T["cost_err"]}</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="msg-sage">⟶ Entrez le nom d\'une ville.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="no-result">Tapez une ville ci-dessus et cliquez sur Calculer.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ONGLET 3 — MÉTÉO (composants natifs Streamlit)
# ══════════════════════════════════════════════
with tab_weather:
    st.markdown(f"""
<div class="hero" style="padding:1.2rem 0 1.8rem; margin-bottom:1.5rem;">
  <div class="hero-title" style="font-size:2.2rem;">{T["wx_title"]}</div>
  <div class="hero-sub">{T["wx_sub"]}</div>
</div>
""", unsafe_allow_html=True)

    col_wx, col_wxbtn = st.columns([4, 1])
    with col_wx:
        wx_city = st.text_input(T["wx_input"], placeholder=T["wx_ph"],
                                label_visibility="collapsed")
    with col_wxbtn:
        wx_btn = st.button(T["wx_btn"], use_container_width=True)

    if wx_btn and wx_city.strip():
        wx = get_weather(wx_city.strip())
        if not wx:
            st.markdown(f'<div class="msg-sage">⟶ {T["wx_err"]}</div>', unsafe_allow_html=True)
        else:
            # ── En-tête : ville + emoji + description ──
            st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            border-bottom:1px solid var(--border);padding-bottom:1rem;margin-bottom:1.2rem;">
  <div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:400;
                color:var(--ink);line-height:1;">{wx["city"]}</div>
    <div style="font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;
                color:var(--muted);margin-top:4px;">{wx["desc"]}</div>
  </div>
  <div style="font-size:3.5rem;line-height:1;">{wx["emoji"]}</div>
</div>
""", unsafe_allow_html=True)

            # ── Température principale ──
            col_t, col_mm = st.columns([2, 1])
            with col_t:
                st.markdown(f"""
<div style="font-family:'Cormorant Garamond',serif;font-size:5rem;font-weight:300;
            color:var(--ink);line-height:1;margin-bottom:4px;">{wx["temp"]}°C</div>
""", unsafe_allow_html=True)
            with col_mm:
                st.markdown(f"""
<div style="padding-top:1.2rem;">
  <div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);">Max · Min</div>
  <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--ink);">
    {wx["temp_max"]}° · {wx["temp_min"]}°
  </div>
</div>
""", unsafe_allow_html=True)

            st.markdown("<div style='height:1px;background:var(--border);margin:1rem 0'></div>", unsafe_allow_html=True)

            # ── 4 métriques en colonnes natives ──
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric(T["wx_feels"],   f"{wx['feels']}°C")
            with c2:
                st.metric(T["wx_humidity"],f"{wx['humidity']} %")
            with c3:
                st.metric(T["wx_wind"],    f"{wx['wind']} km/h")
            with c4:
                st.metric(f"{T['wx_sunrise']} · {T['wx_sunset']}",
                          f"{wx['sunrise']} · {wx['sunset']}")

            st.markdown(f"""
<div style="font-size:0.65rem;letter-spacing:0.07em;color:var(--muted);
            text-align:center;margin-top:1.2rem;">{T["wx_src"]}</div>
""", unsafe_allow_html=True)

    elif wx_btn:
        st.markdown(f'<div class="msg-sage">⟶ {T["wx_err"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="no-result">{T["wx_prompt"]}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ONGLET 4 — BACKPACKER
# ══════════════════════════════════════════════

# Coûts de vols inter-régions (€ aller-retour estimé par tronçon)
VOL_INTER = {
    ("Europe","Europe"):30, ("Europe","Asie"):450, ("Europe","Afrique"):300,
    ("Europe","Amériques"):500, ("Europe","Océanie"):900, ("Europe","Moyen-Orient"):250,
    ("Asie","Asie"):120, ("Asie","Afrique"):500, ("Asie","Amériques"):700,
    ("Asie","Océanie"):350, ("Asie","Moyen-Orient"):200,
    ("Afrique","Afrique"):150, ("Afrique","Amériques"):700, ("Afrique","Océanie"):900,
    ("Amériques","Amériques"):180, ("Amériques","Océanie"):700,
    ("Océanie","Océanie"):200, ("Moyen-Orient","Moyen-Orient"):150,
}
def cout_vol(r1, r2):
    key = tuple(sorted([r1, r2]))
    return VOL_INTER.get(key, VOL_INTER.get((r1,r2), 400))

REGION_MAP = {
    "Asie du Sud-Est": "Asie", "Southeast Asia": "Asie",
    "Europe de l'Est": "Europe", "Eastern Europe": "Europe",
    "Amérique Latine": "Amériques", "Latin America": "Amériques",
    "Afrique": "Afrique", "Africa": "Afrique",
    "Océanie": "Océanie", "Oceania": "Océanie",
    "Moyen-Orient": "Moyen-Orient", "Middle East": "Moyen-Orient",
    "Asia del Sudeste": "Asie", "Europa del Este": "Europe",
    "América Latina": "Amériques", "África": "Afrique",
    "Oceanía": "Océanie", "Oriente Medio": "Moyen-Orient",
}
PAYS_REGION = {
    "Japon":"Asie","Thaïlande":"Asie","Vietnam":"Asie","Cambodge":"Asie","Laos":"Asie",
    "Malaisie":"Asie","Singapour":"Asie","Indonésie":"Asie","Philippines":"Asie",
    "Inde":"Asie","Népal":"Asie","Sri Lanka":"Asie","Chine":"Asie","Corée du Sud":"Asie",
    "Taïwan":"Asie","Mongolie":"Asie","Ouzbékistan":"Asie","Myanmar":"Asie",
    "Géorgie":"Asie","Arménie":"Asie","Azerbaïdjan":"Asie","Maldives":"Asie",
    "France":"Europe","Espagne":"Europe","Italie":"Europe","Portugal":"Europe",
    "Grèce":"Europe","Croatie":"Europe","République Tchèque":"Europe","Hongrie":"Europe",
    "Autriche":"Europe","Pays-Bas":"Europe","Allemagne":"Europe","Suisse":"Europe",
    "Suède":"Europe","Danemark":"Europe","Norvège":"Europe","Finlande":"Europe",
    "Islande":"Europe","Pologne":"Europe","Roumanie":"Europe","Bulgarie":"Europe",
    "Serbie":"Europe","Monténégro":"Europe","Albanie":"Europe","Malte":"Europe",
    "Chypre":"Europe","Turquie":"Europe","Royaume-Uni":"Europe","Irlande":"Europe",
    "États-Unis":"Amériques","Canada":"Amériques","Mexique":"Amériques",
    "Costa Rica":"Amériques","Cuba":"Amériques","Panama":"Amériques","Colombie":"Amériques",
    "Pérou":"Amériques","Bolivie":"Amériques","Brésil":"Amériques","Argentine":"Amériques",
    "Chili":"Amériques","Uruguay":"Amériques","Équateur":"Amériques",
    "Maroc":"Afrique","Tunisie":"Afrique","Égypte":"Afrique","Tanzanie":"Afrique",
    "Kenya":"Afrique","Ouganda":"Afrique","Rwanda":"Afrique","Afrique du Sud":"Afrique",
    "Zimbabwe":"Afrique","Botswana":"Afrique","Madagascar":"Afrique","Seychelles":"Afrique",
    "Maurice":"Afrique","France (Réunion)":"Afrique","Cap-Vert":"Afrique","Sénégal":"Afrique",
    "Éthiopie":"Afrique","Ghana":"Afrique","France":"Europe",
    "Australie":"Océanie","Nv-Zélande":"Océanie","Fidji":"Océanie",
    "Polynésie Fr.":"Océanie","Nv-Calédonie":"Océanie","Papouasie":"Océanie",
    "ÉAU":"Moyen-Orient","Jordanie":"Moyen-Orient","Israël":"Moyen-Orient",
    "Oman":"Moyen-Orient","Qatar":"Moyen-Orient",
}

STYLE_COEF = {"Économique 🌿":0.6, "Équilibré ⚖️":1.0, "Confort 🛎":1.6,
              "Budget 🌿":0.6, "Balanced ⚖️":1.0, "Comfort 🛎":1.6,
              "Económico 🌿":0.6, "Equilibrado ⚖️":1.0, "Confort 🛎":1.6}

def build_backpacker_itinerary(budget, nb_days, style, regions_pref):
    coef = STYLE_COEF.get(style, 1.0)
    regions_filter = [REGION_MAP.get(r) for r in regions_pref] if regions_pref else None

    # Filtrer et scorer les destinations
    pool = []
    for d in DESTINATIONS:
        region = PAYS_REGION.get(d["pays"])
        if not region:
            continue
        if regions_filter and region not in regions_filter:
            continue
        cost_day = COST_DB.get(d["nom"].lower(), COST_DB.get(d["booking_id"].lower()))
        if not cost_day:
            cost_day = {"repas": 20, "transport": 6, "logement": 40, "loisirs": 12}
        pool.append({**d, "region": region, "cost_day": cost_day})

    if not pool:
        return None

    # Construire l'itinéraire : alterner les régions, varier les pays
    import random
    random.seed(42)
    random.shuffle(pool)

    # Nombre de destinations selon budget et durée
    n_dest = max(2, min(8, nb_days // 5))
    # Essayer de varier les régions
    chosen, seen_pays = [], set()
    for d in pool:
        if d["pays"] not in seen_pays:
            chosen.append(d)
            seen_pays.add(d["pays"])
        if len(chosen) >= n_dest:
            break
    if len(chosen) < 2:
        chosen = pool[:n_dest]

    # Distribuer les jours
    days_each = nb_days // len(chosen)
    extra     = nb_days % len(chosen)

    # Calculer les coûts
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
        itinerary.append({
            "dest":   dest,
            "nuits":  nuits,
            "vol":    vol,
            "hotel":  hotel,
            "life":   life,
            "subtot": subtot,
        })
    return itinerary, total_cost


with tab_bpack:
    st.markdown(f"""
<div class="hero" style="padding:1.2rem 0 1.8rem; margin-bottom:1.5rem;">
  <div class="hero-title" style="font-size:2.2rem;">{T["bp_title"]}</div>
  <div class="hero-sub">{T["bp_sub"]}</div>
</div>
""", unsafe_allow_html=True)

    col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
    with col_b1:
        bp_budget = st.slider(T["bp_budget"], 500, 15000, 4000, 100)
    with col_b2:
        bp_days = st.number_input(T["bp_days"], min_value=7, max_value=365, value=30, step=1)
    with col_b3:
        bp_style = st.selectbox(T["bp_style"], T["bp_styles"])

    bp_regions = st.multiselect(T["bp_region"], T["bp_regions"])
    bp_btn = st.button(T["bp_btn"], use_container_width=True)

    if bp_btn:
        result = build_backpacker_itinerary(bp_budget, bp_days, bp_style, bp_regions)
        if not result:
            st.markdown(f'<div class="msg-sage">⟶ {T["bp_warning"]}</div>', unsafe_allow_html=True)
        else:
            itinerary, total_cost = result
            over_budget = total_cost > bp_budget

            # Résumé global
            st.markdown(f"""
<div class="summary">
  <b>{len(itinerary)}</b> pays &nbsp;·&nbsp;
  <b>{bp_days}</b> jours &nbsp;·&nbsp;
  <b style="color:{'#B85555' if over_budget else '#4A6E4E'};">{total_cost:,} €</b>
  {'⚠ dépasse votre budget' if over_budget else '✓ dans votre budget'}
</div>
""", unsafe_allow_html=True)

            # Cartes par destination
            cols = st.columns(min(len(itinerary), 3))
            for idx, step in enumerate(itinerary):
                dest = step["dest"]
                photo = DEST_PHOTOS.get(dest["nom"],
                    "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&q=80")
                with cols[idx % 3]:
                    st.markdown(f"""
<div class="dest-card">
  <div class="photo-wrap">
    <img class="dest-photo" src="{photo}" alt="{dest['nom']}" loading="lazy"
         style="height:140px;">
    <div style="position:absolute;bottom:10px;left:12px;
                background:rgba(13,13,13,0.72);color:#F5F0E8;
                font-size:0.65rem;letter-spacing:0.1em;text-transform:uppercase;
                padding:3px 10px;">{T["bp_nights"].format(n=step["nuits"])}</div>
  </div>
  <div class="dest-body" style="padding:0.9rem 1.1rem 0.8rem;">
    <div class="dest-name" style="font-size:1.3rem;">{dest["flag"]} {dest["nom"]}</div>
    <div class="dest-country">{dest["pays"]}</div>
    <div style="display:flex;flex-direction:column;gap:5px;margin:0.7rem 0;
                font-size:0.72rem;color:var(--muted);">
      <div style="display:flex;justify-content:space-between;">
        <span>✈ {T["bp_flight"]}</span>
        <span style="font-family:'Cormorant Garamond',serif;font-size:0.95rem;color:var(--ink);">{step["vol"]:,} €</span>
      </div>
      <div style="display:flex;justify-content:space-between;">
        <span>🏨 {T["bp_hotel"]}</span>
        <span style="font-family:'Cormorant Garamond',serif;font-size:0.95rem;color:var(--ink);">{step["hotel"]:,} €/nuit</span>
      </div>
      <div style="display:flex;justify-content:space-between;">
        <span>🍽 {T["bp_life"]}</span>
        <span style="font-family:'Cormorant Garamond',serif;font-size:0.95rem;color:var(--ink);">{step["life"]:,} €/jour</span>
      </div>
    </div>
    <div class="dest-price-row" style="padding-top:0.6rem;margin-bottom:0.7rem;">
      <div>
        <div style="font-size:0.65rem;letter-spacing:0.07em;text-transform:uppercase;color:var(--muted);">{T["bp_total_dest"]}</div>
        <div class="dest-price" style="font-size:1.6rem;">{step["subtot"]:,} €</div>
      </div>
    </div>
    <div style="display:flex;gap:6px;">
      <div style="flex:1;">
""", unsafe_allow_html=True)
                    st.link_button(T["btn_sky"], build_skyscanner_url(
                        "CDG", dest["iata"], "20260901", "20260930", 1, 0, 0),
                        use_container_width=True)
                    st.markdown("</div><div style='flex:1;'>", unsafe_allow_html=True)
                    st.link_button(T["btn_book"], build_booking_url(
                        dest["booking_id"], "2026-09-01", "2026-09-30", 1, 0),
                        use_container_width=True)
                    st.markdown("</div></div></div></div>", unsafe_allow_html=True)

            # Récap budget total
            pct = min(100, round(total_cost / bp_budget * 100))
            st.markdown(f"""
<div class="dest-card" style="margin-top:1.5rem;">
  <div class="dest-body">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.8rem;">
      <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;">{T["bp_grand"]}</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:var(--ink);">{total_cost:,} € <span style="font-size:1rem;color:var(--muted);">/ {bp_budget:,} €</span></div>
    </div>
    <div style="height:4px;background:var(--border);margin-bottom:0.6rem;">
      <div style="height:4px;width:{pct}%;background:{'#B85555' if over_budget else '#7A9E7E'};"></div>
    </div>
    <div style="font-size:0.65rem;letter-spacing:0.07em;color:var(--muted);text-align:center;">{T["bp_src"]}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="no-result">{T["bp_prompt"]}</div>', unsafe_allow_html=True)
