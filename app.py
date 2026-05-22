import streamlit as st
import urllib.parse
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="Pouch", page_icon="✈️", layout="centered")

# Dictionnaire de traduction automatique pour l'interface de Pouch
translations = {
    "Français": {
        "title": "✈️ Pouch",
        "subtitle": "Le comparateur qui trouve des voyages selon votre budget réel, pas seulement le prix du vol.",
        "depart": "🛫 Ville de départ",
        "destination": "📍 Destination précise (Optionnel - Laissez vide pour avoir des suggestions)",
        "budget": "💰 Budget TOTAL maximum (€)",
        "date_dep": "🗓️ Date de départ",
        "date_ret": "🗓️ Date de retour",
        "adults": "👨‍💼 Nombre d'adultes",
        "children": "👶 Nombre d'enfants",
        "button": "Trouver mes destinations mondiales",
        "error_date": "La date de retour doit être après la date de départ.",
        "success": "Voici les destinations mondiales valides pour {total} personnes :",
        "vols": "Vols",
        "logement": "Logement",
        "vie": "Vie sur place",
        "meteo": "Météo prévue",
        "meteo_txt": "Consultez le climat local avant votre départ.",
        "reste": "VOTRE RESTE-À-VIVRE",
        "btn_vol": "✈️ Rechercher le vol pour {ville}",
        "btn_hotel": "🏨 Réserver l'hôtel à {ville}",
        "warning_no_dest": "Aucune destination mondiale ne correspond à ce budget pour ces dates.",
        "tab_all": "🌍 Toutes",
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 Amérique",
        "tab_as": "🌏 Asie & Afrique"
    },
    "English": {
        "title": "✈️ Pouch",
        "subtitle": "The comparator that finds trips based on your real budget, not just the flight price.",
        "depart": "🛫 Departure City",
        "destination": "📍 Specific Destination (Optional - Leave blank for suggestions)",
        "budget": "💰 Maximum TOTAL Budget (€)",
        "date_dep": "🗓️ Departure Date",
        "date_ret": "🗓️ Return Date",
        "adults": "👨‍💼 Number of Adults",
        "children": "👶 Number of Children",
        "button": "Find my worldwide destinations",
        "error_date": "Return date must be after departure date.",
        "success": "Here are the valid worldwide destinations for {total} people:",
        "vols": "Flights",
        "logement": "Accommodation",
        "vie": "Cost of living",
        "meteo": "Expected Weather",
        "meteo_txt": "Check local weather conditions before traveling.",
        "reste": "YOUR POCKET MONEY",
        "btn_vol": "✈️ Search flights to {ville}",
        "btn_hotel": "🏨 Book hotel in {ville}",
        "warning_no_dest": "No worldwide destinations match this budget for these dates.",
        "tab_all": "🌍 All",
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 America",
        "tab_as": "🌏 Asia & Africa"
    },
    "Español": {
        "title": "✈️ Pouch",
        "subtitle": "El comparador que encuentra viajes basados en tu presupuesto real, no solo en el precio del vuelo.",
        "depart": "🛫 Ciudad de salida",
        "destination": "📍 Destino específico (Opcional - Dejar en blanco para sugerencias)",
        "budget": "💰 Presupuesto TOTAL máximo (€)",
        "date_dep": "Fecha de salida",
        "date_ret": "Fecha de regreso",
        "adults": "👨‍💼 Número de adultos",
        "children": "👶 Número de niños",
        "button": "Buscar mis destinos mundiales",
        "error_date": "La fecha de regreso debe ser posterior a la fecha de salida.",
        "success": "Aquí están los destinos mundiales válidos para {total} personas:",
        "vols": "Vuelos",
        "logement": "Alojamiento",
        "vie": "Coste de vida",
        "meteo": "Clima previsto",
        "meteo_txt": "Consulte el clima local antes de su viaje.",
        "reste": "TU DINERO DE BOLSILLO",
        "btn_vol": "✈️ Buscar vuelos a {ville}",
        "btn_hotel": "🏨 Reservar hotel en {ville}",
        "warning_no_dest": "Ningún destino mundial coincide con este presupuesto para estas fechas.",
        "tab_all": "🌍 Todas",
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

# Formulaire utilisateur propre
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
        
    destination_saisie = st.text_input(lang["destination"], "")
    submit_button = st.form_submit_button(label=lang["button"])

# Fonction réutilisable pour afficher une carte de destination avec ses boutons propres
def afficher_destination(ville, infos):
    cout_vol = infos["vol"] * total_voyageurs
    cout_hotel = infos["hotel"] * nb_jours * (1 if total_voyageurs <= 2 else 2)
    cout_vie = infos["vie"] * (nb_jours + 1) * total_voyageurs
    total_estime = cout_vol + cout_hotel + cout_vie
    
    if total_estime <= budget:
        reste_a_vivre = budget - total_estime
        nom_pays = f", {infos['pays'][langue]}" if infos['pays'][langue] else ""
        
        st.markdown(f"### 📍 {ville}{nom_pays}")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"- **✈️ {lang['vols']} ({total_voyageurs} pers.)** : {cout_vol}€")
            st.markdown(f"- **🏨 {lang['logement']} ({nb_jours} nuits)** : {cout_hotel}€")
            st.markdown(f"- **🍔 {lang['vie']} ({nb_jours+1} j.)** : {cout_vie}€")
        with col_c2:
            st.info(f"🌤️ **{lang['meteo']}** : {infos['meteo']}")
            st.metric(label=f"🔥 {lang['reste']}", value=f"{reste_a_vivre}€")
        if infos['avis']:
            st.markdown(f"*{infos['avis']}*")
        
        city_encoded = urllib.parse.quote(infos["query"])
        link_vol_strict = "https://skyscanner.fr"
        link_hotel_strict = f"https://booking.com{city_encoded}&lang={lang['lang_booking']}&checkin={str_debut}&checkout={str_fin}&group_adults={adultes}&group_children={enfants}"
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.link_button(lang["btn_vol"].format(ville=ville), link_vol_strict)
        with col_b2:
            st.link_button(lang["btn_hotel"].format(ville=ville), link_hotel_strict)
        st.markdown("---")
        return True
    return False

if submit_button:
    total_voyageurs = adultes + enfants
    nb_jours = (date_fin - date_debut).days
    
    if nb_jours <= 0:
        st.error(lang["error_date"])
    else:
        str_debut = date_debut.strftime("%Y-%m-%d")
        str_fin = date_fin.strftime("%Y-%m-%d")
        
        # Base de données complète et classée par continent
        destinations_globales = {
            "Europe": {
                "Cracovie": {"query": "Krakow", "pays": {"Français": "Pologne", "English": "Poland", "Español": "Polonia"}, "vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ Ensoleillé - 22°C", "avis": "Très économique / Highly affordable"},
                "Budapest": {"query": "Budapest", "pays": {"Français": "Hongrie", "English": "Hungary", "Español": "Hungría"}, "vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ Nuageux - 20°C", "avis": "Magnifique & Pas cher / Great & Cheap"},
                "Porto": {"query": "Porto", "pays": {"Français": "Portugal", "English": "Portugal", "Español": "Portugal"}, "vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 Grand soleil - 25°C", "avis": "Parfait pour le soleil / Perfect for sun"},
                "Sofia": {"query": "Sofia", "pays": {"Français": "Bulgarie", "English": "Bulgaria", "Español": "Bulgaria"}, "vol": 110, "hotel": 35, "vie": 20, "meteo": "🌤️ Climat agréable - 21°C", "avis": "Une des capitales les moins chères"}
            },
            "Amerique": {
                "New York": {"query": "New York", "pays": {"Français": "États-Unis", "English": "USA", "Español": "Estados Unidos"}, "vol": 450, "hotel": 160, "vie": 70, "meteo": "🗽 Ensoleillé - 23°C", "avis": "La métropole mythique américaine"},
                "Montréal": {"query": "Montreal", "pays": {"Français": "Canada", "English": "Canada", "Español": "Canadá"}, "vol": 400, "hotel": 110, "vie": 50, "meteo": "🍁 Beau temps - 21°C", "avis": "Une superbe métropole francophone en Amérique"}
            },
            "AsieAfrique": {
                "Marrakech": {"query": "Marrakech", "pays": {"Français": "Maroc", "English": "Morocco", "Español": "Marruecos"}, "vol": 120, "hotel": 50, "vie": 25, "meteo": "🌵 Chaud et ensoleillé - 31°C", "avis": "Dépaysement total à petit prix"},
                "Tokyo": {"query": "Tokyo", "pays": {"Français": "Japon", "English": "Japan", "Español": "Japón"}, "vol": 750, "hotel": 90, "vie": 45, "meteo": "🌸 Climat idéal - 19°C", "avis": "Un voyage inoubliable mêlant traditions et modernité"},
                "Bangkok": {"query": "Bangkok", "pays": {"Français": "Thaïlande", "English": "Thailand", "Español": "Tailandia"}, "vol": 600, "hotel": 30, "vie": 15, "meteo": "🌴 Chaud et tropical - 33°C", "avis": "Une expérience exotique incroyable"}
            }
        }
        
        dest_test = destination_saisie.strip().lower()
        st.success(lang["success"].format(total=total_voyageurs))
        
        if dest_test:
            # Recherche précise de l'utilisateur
            cout_vol_unitaire, cout_hotel_nuit, cout_vie_jour = 550, 85, 45
