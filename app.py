import streamlit as st
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="Pouch", page_icon="✈️", layout="centered")

# Dictionnaire de traduction automatique pour l'interface de Pouch
translations = {
    "Français": {
        "title": "✈️ Pouch",
        "subtitle": "Le comparateur qui trouve des voyages selon votre budget réel, pas seulement le prix du vol.",
        "depart": "🛫 Ville de départ",
        "budget": "💰 Budget TOTAL maximum (€)",
        "duration": "🗓️ Durée du voyage (en jours)",
        "adults": "👨‍💼 Nombre d'adultes",
        "children": "👶 Nombre d'enfants",
        "button": "Trouver mes destinations mondiales",
        "success": "Voici les destinations mondiales valides pour {total} personnes :",
        "vols": "Vols",
        "logement": "Logement",
        "vie": "Vie sur place",
        "meteo": "Météo prévue",
        "reste": "VOTRE RESTE-À-VIVRE",
        "btn_vol": "✈️ Rechercher le vol pour {ville}",
        "btn_hotel": "🏨 Réserver l'hôtel à {ville}",
        "warning_no_dest": "Aucune destination mondiale ne correspond à ce budget pour cette durée.",
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 Amérique",
        "tab_as": "🌏 Asie & Afrique"
    },
    "English": {
        "title": "✈️ Pouch",
        "subtitle": "The comparator that finds trips based on your real budget, not just the flight price.",
        "depart": "🛫 Departure City",
        "budget": "💰 Maximum TOTAL Budget (€)",
        "duration": "🗓️ Trip duration (in days)",
        "adults": "👨‍💼 Number of Adults",
        "children": "👶 Number of Children",
        "button": "Find my worldwide destinations",
        "success": "Here are the valid worldwide destinations for {total} people:",
        "vols": "Flights",
        "logement": "Accommodation",
        "vie": "Cost of living",
        "meteo": "Expected Weather",
        "reste": "YOUR POCKET MONEY",
        "btn_vol": "✈️ Search flights to {ville}",
        "btn_hotel": "🏨 Book hotel in {ville}",
        "warning_no_dest": "No worldwide destinations match this budget for this duration.",
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 America",
        "tab_as": "🌏 Asia & Africa"
    },
    "Español": {
        "title": "✈️ Pouch",
        "subtitle": "El comparador que encuentra viajes basados en tu presupuesto real, no solo en el precio del vuelo.",
        "depart": "🛫 Ciudad de salida",
        "budget": "💰 Presupuesto TOTAL máximo (€)",
        "duration": "🗓️ Duración del viaje (en días)",
        "adults": "👨‍💼 Número de adultos",
        "children": "👶 Número de niños",
        "button": "Buscar mis destinos mundiales",
        "success": "Aquí están los destinos mundiales válidos para {total} personas:",
        "vols": "Vuelos",
        "logement": "Alojamiento",
        "vie": "Coste de vida",
        "meteo": "Clima previsto",
        "reste": "TU DINERO DE BOLSILLO",
        "btn_vol": "✈️ Buscar vuelos a {ville}",
        "btn_hotel": "🏨 Reservar hotel en {ville}",
        "warning_no_dest": "Ningún destino mundial coincide con este presupuesto para esta duración.",
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 América",
        "tab_as": "🌏 Asia & África"
    }
}

# Sélecteur de langue global
langue = st.selectbox("🌐 Choose Language / Choisir la Langue / Elegir Idioma", ["Français", "English", "Español"])
lang = translations[langue]

st.title(lang["title"])
st.subheader(lang["subtitle"])

# Formulaire utilisateur ultra-stable
with st.form("budget_form"):
    col1, col2 = st.columns(2)
    with col1:
        depart = st.text_input(lang["depart"], "Paris")
        nb_jours = st.number_input(lang["duration"], min_value=1, value=4, step=1)
        adultes = st.number_input(lang["adults"], min_value=1, value=1, step=1)
    with col2:
        budget = st.number_input(lang["budget"], min_value=50, value=1500, step=50)
        enfants = st.number_input(lang["children"], min_value=0, value=0, step=1)
        
    submit_button = st.form_submit_button(label=lang["button"])

# Fonction d'affichage avec liens en dur absolus (ZÉRO ERREUR TECHNIQUE POSSIBLE)
def afficher_destination(ville, infos, budget, total_voyageurs, nb_jours, link_vol, link_hotel):
    nb_nuits = nb_jours - 1 if nb_jours > 1 else 1
    cout_vol = infos["vol"] * total_voyageurs
    cout_hotel = infos["hotel"] * nb_nuits * (1 if total_voyageurs <= 2 else 2)
    cout_vie = infos["vie"] * nb_jours * total_voyageurs
    total_estime = cout_vol + cout_hotel + cout_vie
    
    if total_estime <= budget:
        reste_a_vivre = budget - total_estime
        nom_pays = f", {infos['pays'][langue]}" if infos['pays'][langue] else ""
        
        st.markdown(f"### 📍 {ville}{nom_pays}")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"- **✈️ {lang['vols']} ({total_voyageurs} pers.)** : {cout_vol}€")
            st.markdown(f"- **🏨 {lang['logement']} ({nb_nuits} nuits)** : {cout_hotel}€")
            st.markdown(f"- **🍔 {lang['vie']} ({nb_jours} j.)** : {cout_vie}€")
        with col_c2:
            st.info(f"🌤️ **{lang['meteo']}** : {infos['meteo']}")
            st.metric(label=f"🔥 {lang['reste']}", value=f"{reste_a_vivre}€")
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.link_button(lang["btn_vol"].format(ville=ville), link_vol)
        with col_b2:
            st.link_button(lang["btn_hotel"].format(ville=ville), link_hotel)
        st.markdown("---")
        return True
    return False

if submit_button:
    total_voyageurs = adultes + enfants
    st.success(lang["success"].format(total=total_voyageurs))
    
    # Base de données fixe et sécurisée
    destinations_globales = {
        "Europe": {
            "Cracovie": {"pays": {"Français": "Pologne", "English": "Poland", "Español": "Polonia"}, "vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ Ensoleillé - 22°C", "query": "Krakow", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"},
            "Budapest": {"pays": {"Français": "Hongrie", "English": "Hungary", "Español": "Hungría"}, "vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ Nuageux - 20°C", "query": "Budapest", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"},
            "Porto": {"pays": {"Français": "Portugal", "English": "Portugal", "Español": "Portugal"}, "vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 Grand soleil - 25°C", "query": "Porto", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"},
            "Sofia": {"pays": {"Français": "Bulgarie", "English": "Bulgaria", "Español": "Bulgaria"}, "vol": 110, "hotel": 35, "vie": 20, "meteo": "🌤️ Climat agréable - 21°C", "query": "Sofia", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"}
        },
        "Amerique": {
            "New York": {"pays": {"Français": "États-Unis", "English": "USA", "Español": "Estados Unidos"}, "vol": 450, "hotel": 160, "vie": 70, "meteo": "🗽 Ensoleillé - 23°C", "query": "New York", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"},
            "Montréal": {"pays": {"Français": "Canada", "English": "Canada", "Español": "Canadá"}, "vol": 400, "hotel": 110, "vie": 50, "meteo": "🍁 Beau temps - 21°C", "query": "Montreal", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"}
        },
        "AsieAfrique": {
            "Marrakech": {"pays": {"Français": "Maroc", "English": "Morocco", "Español": "Marruecos"}, "vol": 120, "hotel": 50, "vie": 25, "meteo": "🌵 Chaud et ensoleillé - 31°C", "query": "Marrakech", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"},
            "Tokyo": {"pays": {"Français": "Japon", "English": "Japan", "Español": "Japón"}, "vol": 750, "hotel": 90, "vie": 45, "meteo": "🌸 Climat idéal - 19°C", "query": "Tokyo", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"},
            "Bangkok": {"pays": {"Français": "Thaïlande", "English": "Thailand", "Español": "Tailandia"}, "vol": 600, "hotel": 30, "vie": 15, "meteo": "🌴 Chaud et tropical - 33°C", "query": "Bangkok", "link_vol": "https://skyscanner.fr", "link_hotel": "https://booking.com"}
        }
    }
    
    tab1, tab2, tab3 = st.tabs([lang["tab_eu"], lang["tab_am"], lang["tab_as"]])
    with tab1:
        for v, i in destinations_globales["Europe"].items():
            afficher_destination(v, i, budget, total_voyageurs, nb_jours, i["link_vol"], i["link_hotel"])
    with tab2:
        for v, i in destinations_globales["Amerique"].items():
            afficher_destination(v, i, budget, total_voyageurs, nb_jours, i["link_vol"], i["link_hotel"])
    with tab3:
        for v, i in destinations_globales["AsieAfrique"].items():
            afficher_destination(v, i, budget, total_voyageurs, nb_jours, i["link_vol"], i["link_hotel"])
