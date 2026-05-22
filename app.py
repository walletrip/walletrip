import streamlit as st
import google.generativeai as genai
from datetime import datetime
import urllib.parse
import json

# Configuration de la page Streamlit
st.set_page_config(page_title="WalletTrip", page_icon="✈️", layout="centered")

# Dictionnaire de traduction automatique pour l'interface
translations = {
    "Français": {
        "title": "✈️ WalletTrip",
        "subtitle": "L'IA mondiale qui trouve des voyages selon votre budget réel, pas seulement le prix du vol.",
        "depart": "🛫 Ville de départ",
        "budget": "💰 Budget TOTAL maximum (€)",
        "date_dep": "🗓️ Date de départ",
        "date_ret": "🗓️ Date de retour",
        "adults": "👨‍💼 Nombre d'adultes",
        "children": "👶 Nombre d'enfants",
        "button": "Voyager dans le monde entier",
        "error_date": "La date de retour doit être après la date de départ.",
        "loading": "L'IA analyse le coût de la vie mondial et prépare vos liens...",
        "success": "Voici les destinations mondiales valides pour {total} personnes :",
        "vols": "Vols",
        "logement": "Logement",
        "vie": "Vie sur place",
        "meteo": "Météo prévue",
        "reste": "VOTRE RESTE-À-VIVRE",
        "btn_vol": "✈️ Rechercher le vol pour {ville}",
        "btn_hotel": "🏨 Réserver l'hôtel à {ville}",
        "lang_booking": "fr"
    },
    "English": {
        "title": "✈️ WalletTrip",
        "subtitle": "The global AI that finds trips based on your real budget, not just the flight price.",
        "depart": "🛫 Departure City",
        "budget": "💰 Maximum TOTAL Budget (€)",
        "date_dep": "🗓️ Departure Date",
        "date_ret": "🗓️ Return Date",
        "adults": "👨‍💼 Number of Adults",
        "children": "👶 Number of Children",
        "button": "Travel worldwide",
        "error_date": "Return date must be after departure date.",
        "loading": "AI is calculating worldwide cost of living and preparing your links...",
        "success": "Here are the valid worldwide destinations for {total} people:",
        "vols": "Flights",
        "logement": "Accommodation",
        "vie": "Cost of living",
        "meteo": "Expected Weather",
        "reste": "YOUR POCKET MONEY",
        "btn_vol": "✈️ Search flights to {ville}",
        "btn_hotel": "🏨 Book hotel in {ville}",
        "lang_booking": "en-us"
    },
    "Español": {
        "title": "✈️ WalletTrip",
        "subtitle": "La IA mundial que encuentra viajes basados en tu presupuesto real, no solo en el precio del vuelo.",
        "depart": "🛫 Ciudad de salida",
        "budget": "💰 Presupuesto TOTAL máximo (€)",
        "date_dep": "Fecha de salida",
        "date_ret": "Fecha de regreso",
        "adults": "👨‍💼 Número de adultos",
        "children": "👶 Número de niños",
        "button": "Viajar por todo el mundo",
        "error_date": "La fecha de regreso debe ser posterior a la fecha de salida.",
        "loading": "La IA está calculando el costo de vida mundial y preparando los enlaces...",
        "success": "Aquí están los destinos mundiales válidos para {total} personas:",
        "vols": "Vuelos",
        "logement": "Alojamiento",
        "vie": "Coste de vida",
        "meteo": "Clima previsto",
        "reste": "TU DINERO DE BOLSILLO",
        "btn_vol": "✈️ Buscar vuelos a {ville}",
        "btn_hotel": "🏨 Reservar hotel en {ville}",
        "lang_booking": "es"
    }
}

# Sélecteur de langue global
langue = st.selectbox("🌐 Choose Language / Choisir la Langue / Elegir Idioma", ["Français", "English", "Español"])
lang = translations[langue]

st.title(lang["title"])
st.subheader(lang["subtitle"])

# Formulaire utilisateur
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
            
            # PROMPT AVEC LE FILTRE MONDIAL ET LE STRUCTURAGE DES NOMS EN ANGLAIS POUR BOOKING
            prompt = f"""
            You are a global travel expert. Write your response ONLY in {langue}.
            Analyse ALL COUNTRIES IN THE WORLD to find 2 or 3 amazing destinations.
            Departure city: {depart}. From {str_debut} to {str_fin} ({nb_jours} nights).
            Total group size: {adultes} adult(s) and {enfants} child(ren) ({total_voyageurs} people total).
            The MAXIMUM TOTAL BUDGET for EVERYTHING (flights + hotel + local life for ALL people) is {budget}€.
            
            Calculate precisely: Flight cost + Hotel cost + (Cost of living per day * {nb_jours+1} * {total_voyageurs}).
            Only output destinations where the sum is LESS than {budget}€.
            
            Provide your response ONLY as a strict JSON array, with no other text before or after:
            [
              {{
                "ville_anglais": "Name of the city in English (Ex: New York, Tokyo, Krakow)",
                "ville_traduit": "Name of the city translated in {langue}",
                "pays": "Name of the country in {langue}",
                "vol_total": 150,
                "hotel_total": 200,
                "vie_totale": 100,
                "reste_argent_poche": 50,
                "meteo": "Weather description in {langue}",
                "avis": "Short justification in {langue}"
              }}
            ]
            """
            
            with st.spinner(lang["loading"]):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    # Nettoyage et lecture sécurisée du JSON de l'IA
                    json_text = response.text.strip().replace("```json", "").replace("```", "")
                    destinations = json.loads(json_text)
                    
                    st.success(lang["success"].format(total=total_voyageurs))
                    
                    for dest in destinations:
                        st.markdown(f"### 📍 {dest['ville_traduit']}, {dest['pays']}")
                        
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            st.markdown(f"- **✈️ {lang['vols']} ({total_voyageurs} pers.)** : {dest['vol_total']}€")
                            st.markdown(f"- **🏨 {lang['logement']} ({nb_jours} nuits)** : {dest['hotel_total']}€")
                            st.markdown(f"- **🍔 {lang['vie']} ({nb_jours+1} j.)** : {dest['vie_totale']}€")
                        with col_c2:
                            st.info(f"🌤️ **{lang['meteo']}** : {dest['meteo']}")
                            st.metric(label=f"🔥 {lang['reste']}", value=f"{dest['reste_argent_poche']}€")
                        
                        st.markdown(f"*{dest['avis']}*")
                        
                        # PYTHON SÉCURISE LES LIENS SANS AUCUN RISQUE DE COLLAGE TEXTE
                        city_booking = urllib.parse.quote(dest["ville_anglais"])
                        
                        link_vol = f"https://skyscanner.fr"
                        link_hotel = f"https://booking.com{tp_id}&ss={city_booking}&lang={lang['lang_booking']}&checkin={str_debut}&checkout={str_fin}&group_adults={adultes}&group_children={enfants}"
                        
                        # Un bloc de boutons dédié spécifiquement sous chaque option
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            st.link_button(lang["btn_vol"].format(ville=dest['ville_traduit']), link_vol)
                        with col_b2:
                            st.link_button(lang["btn_hotel"].format(ville=dest['ville_traduit']), link_hotel)
                        st.markdown("---")
                        
                except Exception as e:
                    st.error("Désolé, une erreur est survenue lors de l'analyse. Veuillez relancer la recherche.")
