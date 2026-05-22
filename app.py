import streamlit as st
from datetime import datetime
import urllib.parse

# Configuration de la page Streamlit
st.set_page_config(page_title="WalletTrip", page_icon="✈️", layout="centered")

# Dictionnaire de traduction automatique pour l'interface
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
        "success": "Voici les destinations valides pour {total} personnes :",
        "vols": "Vols",
        "logement": "Logement",
        "vie": "Vie sur place",
        "meteo": "Météo prévue",
        "reste": "VOTRE RESTE-À-VIVRE",
        "btn_vol": "✈️ Voir les vols pour {ville}",
        "btn_hotel": "🏨 Réserver l'hôtel à {ville}"
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
        "success": "Here are the valid destinations for {total} people:",
        "vols": "Flights",
        "logement": "Accommodation",
        "vie": "Cost of living",
        "meteo": "Expected Weather",
        "reste": "YOUR POCKET MONEY",
        "btn_vol": "✈️ See flights to {ville}",
        "btn_hotel": "🏨 Book hotel in {ville}"
    },
    "Español": {
        "title": "✈️ WalletTrip",
        "subtitle": "La IA que encuentra viajes basados en tu presupuesto real, no solo en el precio del vuelo.",
        "depart": "🛫 Ciudad de salida",
        "budget": "💰 Presupuesto TOTAL máximo (€)",
        "date_dep": "Fecha de salida",
        "date_ret": "Fecha de regreso",
        "adults": "👨‍💼 Número de adultos",
        "children": "👶 Número de niños",
        "button": "Buscar mis destinos reales",
        "error_date": "La fecha de regreso debe ser posterior a la fecha de salida.",
        "success": "Aquí están los destinos válidos para {total} personas:",
        "vols": "Vuelos",
        "logement": "Alojamiento",
        "vie": "Coste de vida",
        "meteo": "Clima previsto",
        "reste": "TU DINERO DE BOLSILLO",
        "btn_vol": "✈️ Ver vuelos a {ville}",
        "btn_hotel": "🏨 Reservar hotel en {ville}"
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
    tp_id = st.secrets.get("TRAVELPAYOUTS_ID", "531779")
    total_voyageurs = adultes + enfants
    nb_jours = (date_fin - date_debut).days
    
    if nb_jours <= 0:
        st.error(lang["error_date"])
    else:
        str_debut = date_debut.strftime("%Y-%m-%d")
        str_fin = date_fin.strftime("%Y-%m-%d")
        
        # Base de données stable des coûts par personne
        destinations_data = {
            "Cracovie": {"pays": {"Français": "Pologne", "English": "Poland", "Español": "Polonia"}, "vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ Ensoleillé - 22°C", "avis": "Très économique / Highly affordable / Muy económico"},
            "Budapest": {"pays": {"Français": "Hongrie", "English": "Hungary", "Español": "Hungría"}, "vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ Nuageux - 20°C", "avis": "Magnifique & Pas cher / Great & Cheap / Magnífico y barato"},
            "Porto": {"pays": {"Français": "Portugal", "English": "Portugal", "Español": "Portugal"}, "vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 Grand soleil - 25°C", "avis": "Parfait pour le soleil / Perfect for sun / Perfecto para el sol"}
        }
        
        st.success(lang["success"].format(total=total_voyageurs))
        
        for ville, infos in destinations_data.items():
            # Calculs exacts et proportionnels au nombre de voyageurs et de jours
            cout_vol = infos["vol"] * total_voyageurs
            cout_hotel = infos["hotel"] * nb_jours * (1 if total_voyageurs <= 2 else 2) # Ajoute une chambre si grand groupe
            cout_vie = infos["vie"] * (nb_jours + 1) * total_voyageurs
            total_estime = cout_vol + cout_hotel + cout_vie
            
            # Filtre de l'enveloppe budgétaire
            if total_estime <= budget:
                reste_a_vivre = budget - total_estime
                
                st.markdown(f"### 📍 {ville}, {infos['pays'][langue]}")
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown(f"- **✈️ {lang['vols']} ({total_voyageurs} pers.)** : {cout_vol}€")
                    st.markdown(f"- **🏨 {lang['logement']} ({nb_jours} nuits)** : {cout_hotel}€")
                    st.markdown(f"- **🍔 {lang['vie']} ({nb_jours+1} j.)** : {cout_vie}€")
                with col_c2:
                    st.info(f"🌤️ **{lang['meteo']}** : {infos['meteo']}")
                    st.metric(label=f"🔥 {lang['reste']}", value=f"{reste_a_vivre}€")
                
                st.markdown(f"*{infos['avis']}*")
                
                # Génération des boutons de redirection parfaits et multilingues
                city_enc = urllib.parse.quote(ville)
                dep_enc = urllib.parse.quote(depart)
                
                link_vol = f"https://skyscanner.fr{dep_enc}/{city_enc}/"
                link_hotel = f"https://booking.com{tp_id}&ss={city_enc}&checkin={str_debut}&checkout={str_fin}&group_adults={adultes}&group_children={enfants}"
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.link_button(lang["btn_vol"].format(ville=ville), link_vol)
                with col_b2:
                    st.link_button(lang["btn_hotel"].format(ville=ville), link_hotel)
                st.markdown("---")
