import streamlit as st
import google.generativeai as genai
from datetime import datetime
import urllib.parse
import json

# Configuration de la page Streamlit
st.set_page_config(page_title="WalletTrip", page_icon="✈️", layout="centered")

# Dictionnaire de traduction pour l'interface de l'application
translations = {
    "Français": {
        "title": "✈️ WalletTrip",
        "subtitle": "L'IA qui trouve des voyages selon votre budget réel, pas seulement le prix du vol.",
        "depart": "🛫 Ville de départ",
        "budget": "💰 Budget TOTAL maximum (€)",
        "date_dep": "🗓️ Date de départ",
        "date_ret": "🗓️ Date de retour",
        "adults": "👨‍💼 Nombre d'adultes",
        "children": "👶 Nombre d'enfants",
        "button": "Trouver mes destinations réelles",
        "error_date": "La date de retour doit être après la date de départ.",
        "loading": "L'IA calcule le budget de groupe et analyse la météo locale...",
        "success": "Voici les destinations valides pour {total} personnes :",
        "vols": "Vols",
        "logement": "Logement",
        "vie": "Vie sur place",
        "meteo": "Météo prévue",
        "reste": "VOTRE RESTE-À-VIVRE",
        "btn_vol": "✈️ Voir les vols pour {ville}",
        "btn_hotel": "🏨 Réserver l'hôtel à {ville}",
        "domain_booking": "fr.html?aid=",
        "domain_sky": "fr"
    },
    "English": {
        "title": "✈️ WalletTrip",
        "subtitle": "The AI that finds trips based on your real budget, not just the flight price.",
        "depart": "🛫 Departure City",
        "budget": "💰 Maximum TOTAL Budget (€)",
        "date_dep": "🗓️ Departure Date",
        "date_ret": "🗓️ Return Date",
        "adults": "👨‍💼 Number of Adults",
        "children": "👶 Number of Children",
        "button": "Find my real destinations",
        "error_date": "Return date must be after departure date.",
        "loading": "AI is calculating group budget and analyzing local weather...",
        "success": "Here are the valid destinations for {total} people:",
        "vols": "Flights",
        "logement": "Accommodation",
        "vie": "Cost of living",
        "meteo": "Expected Weather",
        "reste": "YOUR POCKET MONEY",
        "btn_vol": "✈️ See flights to {ville}",
        "btn_hotel": "🏨 Book hotel in {ville}",
        "domain_booking": "en.html?aid=",
        "domain_sky": "net"
    },
    "Español": {
        "title": "✈️ WalletTrip",
        "subtitle": "La IA que encuentra viajes basados en tu presupuesto real, no solo en el precio del vuelo.",
        "depart": "🛫 Ciudad de salida",
        "budget": "💰 Presupuesto TOTAL máximo (€)",
        "date_dep": "🗓️ Fecha de salida",
        "date_ret": "🗓️ Fecha de regreso",
        "adults": "👨‍💼 Número de adultos",
        "children": "👶 Número de niños",
        "button": "Buscar mis destinos reales",
        "error_date": "La fecha de regreso debe ser posterior a la fecha de salida.",
        "loading": "La IA está calculando el presupuesto grupal y analizando el clima...",
        "success": "Aquí están los destinos válidos para {total} personas:",
        "vols": "Vuelos",
        "logement": "Alojamiento",
        "vie": "Coste de vida",
        "meteo": "Clima previsto",
        "reste": "TU DINERO DE BOLSILLO",
        "btn_vol": "✈️ Ver vuelos a {ville}",
        "btn_hotel": "🏨 Reservar hotel en {ville}",
        "domain_booking": "es.html?aid=",
        "domain_sky": "es"
    }
}

# Sélecteur de langue tout en haut de la page
langue = st.selectbox("🌐 Choose Language / Choisir la Langue / Elegir Idioma", ["Français", "English", "Español"])
lang = translations[langue]

st.title(lang["title"])
st.subheader(lang["subtitle"])

# Formulaire dynamique traduit automatiquement
with st.form("budget_form"):
    col1, col2 = st.columns(2)
    with col1:
        depart = st.text_input(lang["depart"], "Paris")
        date_debut = st.date_input(lang["date_dep"], datetime.today())
        adultes = st.number_input(lang["adults"], min_value=1, value=1, step=1)
    with col2:
        budget = st.number_input(lang["budget"], min_value=50, value=500, step=50)
        date_fin = st.date_input(lang["date_ret"], datetime.today())
        enfants = st.number_input(lang["children"], min_value=0, value=0, step=1)
        
    submit_button = st.form_submit_button(label=lang["button"])

# Traitement de la demande
if submit_button:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Veuillez configurer votre clé API Gemini (GEMINI_API_KEY) dans les paramètres.")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        tp_id = st.secrets.get("TRAVELPAYOUTS_ID", "531779")
        
        total_voyageurs = adultes + enfants
        nb_jours = (date_fin - date_debut).days
        
        if nb_jours <= 0:
            st.error(lang["error_date"])
        else:
            str_debut = date_debut.strftime("%Y-%m-%d")
            str_fin = date_fin.strftime("%Y-%m-%d")
            
            # Consigne stricte à l'IA de répondre dans la langue choisie
            prompt = f"""
            You are a world travel agent assistant. Write your response ONLY in {langue}.
            A user wants to travel from {depart} from {str_debut} to {str_fin} ({nb_jours} nights).
            There are {adultes} adult(s) and {enfants} child(ren) ({total_voyageurs} people total).
            The maximum total budget for EVERYTHING (flights + hotels + meals for everyone) is {budget}€.
            
            Find 2 or 3 real destinations in Europe where the total price fits inside the budget.
            Estimate typical weather conditions for that city during this period.
            
            Provide your response ONLY as a strict JSON array, with no other text before or after:
            [
              {{
                "ville": "Name of the city in English",
                "pays": "Name of the country translated in {langue}",
                "vol_total": 140,
                "hotel_total": 240,
                "vie_totale": 180,
                "reste_argent_poche": 40,
                "meteo": "Weather description in {langue}",
                "avis": "Short justification in {langue}"
              }}
            ]
            """
            
            with st.spinner(lang["loading"]):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    json_text = response.text.strip().replace("```json", "").replace("```", "")
                    destinations = json.loads(json_text)
                    
                    st.success(lang["success"].format(total=total_voyageurs))
                    
                    for dest in destinations:
                        st.markdown(f"### 📍 {dest['ville']}, {dest['pays']}")
                        
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            st.markdown(f"- **✈️ {lang['vols']} ({total_voyageurs} pers.)** : {dest['vol_total']}€")
                            st.markdown(f"- **🏨 {lang['logement']} ({nb_jours} nuits)** : {dest['hotel_total']}€")
                            st.markdown(f"- **🍔 {lang['vie']} ({nb_jours+1} j.)** : {dest['vie_totale']}€")
                        with col_c2:
                            st.info(f"🌤️ **{lang['meteo']}** : {dest['meteo']}")
                            st.metric(label=f"🔥 {lang['reste']}", value=f"{dest['reste_argent_poche']}€")
                        
                        st.markdown(f"*{dest['avis']}*")
                        
                        # Liens internationaux dynamiques adaptés à la langue sélectionnée
                        city_enc = urllib.parse.quote(dest['ville'])
                        dep_enc = urllib.parse.quote(depart)
                        
                        link_vol = f"https://www.skyscanner.{lang['domain_sky']}/transport/vols/{dep_enc}/{city_enc}/"
                        link_hotel = f"https://booking.com.{lang['domain_booking']}{tp_id}&ss={city_enc}&checkin={str_debut}&checkout={str_fin}&group_adults={adultes}&group_children={enfants}"
                        
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            st.link_button(lang["btn_vol"].format(ville=dest['ville']), link_vol)
                        with col_b2:
                            st.link_button(lang["btn_hotel"].format(ville=dest['ville']), link_hotel)
                        st.markdown("---")
                        
                except Exception as e:
                    st.markdown(response.text)
