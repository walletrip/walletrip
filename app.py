import streamlit as st
import urllib.parse
from datetime import datetime

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
        "btn_vol": "✈️ Vols directs pour {ville}",
        "btn_hotel": "🏨 Hôtels disponibles à {ville}",
        "domain_booking": "fr.html",
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
        "success": "Here are the valid destinations for {total} people:",
        "vols": "Flights",
        "logement": "Accommodation",
        "vie": "Cost of living",
        "meteo": "Expected Weather",
        "reste": "YOUR POCKET MONEY",
        "btn_vol": "✈️ Direct flights to {ville}",
        "btn_hotel": "🏨 Available hotels in {ville}",
        "domain_booking": "en.html",
        "domain_sky": "net"
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
        "btn_vol": "✈️ Vuelos directos a {ville}",
        "btn_hotel": "🏨 Hoteles disponibles en {ville}",
        "domain_booking": "es.html",
        "domain_sky": "es"
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
        
        # Base de données fixe et ultra-sécurisée avec les codes de destinations Skyscanner (ex: krk pour cracovie)
        destinations_data = {
            "Cracovie": {"code_sky": "krk", "search_booking": "Krakow", "pays": {"Français": "Pologne", "English": "Poland", "Español": "Polonia"}, "vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ Ensoleillé - 22°C", "avis": "Très économique / Highly affordable / Muy económico"},
            "Budapest": {"code_sky": "bud", "search_booking": "Budapest", "pays": {"Français": "Hongrie", "English": "Hungary", "Español": "Hungría"}, "vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ Nuageux - 20°C", "avis": "Magnifique & Pas cher / Great & Cheap / Magnífico y barato"},
            "Porto": {"code_sky": "opo", "search_booking": "Porto", "pays": {"Français": "Portugal", "English": "Portugal", "Español": "Portugal"}, "vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 Grand soleil - 25°C", "avis": "Parfait pour le soleil / Perfect for sun / Perfecto para el sol"},
            "Marrakech": {"code_sky": "rak", "search_booking": "Marrakech", "pays": {"Français": "Maroc", "English": "Morocco", "Español": "Marruecos"}, "vol": 120, "hotel": 50, "vie": 30, "meteo": "🌵 Chaud et ensoleillé - 31°C", "avis": "Dépaysement total à petit prix / Total change of scenery / Desconexión total"},
            "Sofia": {"code_sky": "sof", "search_booking": "Sofia", "pays": {"Français": "Bulgarie", "English": "Bulgaria", "Español": "Bulgaria"}, "vol": 110, "hotel": 35, "vie": 22, "meteo": "🌤️ Climat agréable - 21°C", "avis": "Une des capitales les moins chères / One of the cheapest capitals / Una de las capitales más baratas"}
        }
        
        st.success(lang["success"].format(total=total_voyageurs))
        
        # Nettoyage de la ville de départ saisie par l'utilisateur pour le lien Skyscanner
        depart_clean = depart.strip().lower().replace(" ", "")
        if not depart_clean:
            depart_clean = "paris"
            
        for ville, infos in destinations_data.items():
            # Calculs du coût du groupe
            cout_vol = infos["vol"] * total_voyageurs
            cout_hotel = infos["hotel"] * nb_jours * (1 if total_voyageurs <= 2 else 2)
            cout_vie = infos["vie"] * (nb_jours + 1) * total_voyageurs
            total_estime = cout_vol + cout_hotel + cout_vie
            
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
                
                # FABRICATION DES LIENS ULTRA-PRÉCIS PAR DESTINATION ET PARTICIPANTS
                city_encoded_booking = urllib.parse.quote(infos["search_booking"])
                
                # Lien direct Skyscanner configuré avec la ville de départ, d'arrivée et les dates exactes
                link_vol_strict = f"https://www.skyscanner.{lang['domain_sky']}/transport/vols/{depart_clean}/{infos['code_sky']}/{str_debut[:2]}{str_debut[5:7]}{str_debut[8:10]}/{str_fin[:2]}{str_fin[5:7]}{str_fin[8:10]}/"
                
                # Lien direct Booking configuré avec la ville d'arrivée exacte, les dates et le nombre de participants
                link_hotel_strict = f"https://booking.com.{lang['domain_booking']}?aid={tp_id}&ss={city_encoded_booking}&checkin={str_debut}&checkout={str_fin}&group_adults={adultes}&group_children={enfants}"
                
                # Boutons bleus exclusifs positionnés sous CHAQUE ville proposée
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.link_button(lang["btn_vol"].format(ville=ville), link_vol_strict)
                with col_b2:
                    st.link_button(lang["btn_hotel"].format(ville=ville), link_hotel_strict)
                st.markdown("---")
