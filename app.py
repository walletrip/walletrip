import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

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
        "warning_no_dest": "Aucune destination mondiale ne correspond à ce budget pour ces dates. Essayez d'augmenter votre budget.",
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 Amérique",
        "tab_as": "🌏 Asie & Afrique",
        "lang_booking": "fr"
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
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 America",
        "tab_as": "🌏 Asia & Africa",
        "lang_booking": "en-us"
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
        "tab_eu": "🇪🇺 Europe",
        "tab_am": "🌎 América",
        "tab_as": "🌏 Asia & África",
        "lang_booking": "es"
    }
}

# Sélecteur de langue global
langue = st.selectbox("🌐 Choose Language / Choisir la Langue / Elegir Idioma", ["Français", "English", "Español"])
lang = translations[langue]

st.title(lang["title"])
st.subheader(lang["subtitle"])
# Formulaire utilisateur propre avec le retour des deux calendriers de dates
with st.form("budget_form"):
    col1, col2 = st.columns(2)
    with col1:
        depart = st.text_input(lang["depart"], "Paris")
        date_debut = st.date_input(lang["date_dep"], datetime.today())
        adultes = st.number_input(lang["adults"], min_value=1, value=1, step=1)
    with col2:
        budget = st.number_input(lang["budget"], min_value=50, value=1500, step=50)
        date_fin = st.date_input(lang["date_ret"], datetime.today() + timedelta(days=4))
        enfants = st.number_input(lang["children"], min_value=0, value=0, step=1)
        
    destination_saisie = st.text_input(lang["destination"], "")
    submit_button = st.form_submit_button(label=lang["button"])

# Base de données complète et classée par continent avec les codes aéroports IATA pour Skyscanner
destinations_globales = {
    "Europe": {
        "Cracovie": {"query": "Krakow", "code_iata": "KRK", "pays": {"Français": "Pologne", "English": "Poland", "Español": "Polonia"}, "vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ Ensoleillé - 22°C", "avis": "Très économique / Highly affordable"},
        "Budapest": {"query": "Budapest", "code_iata": "BUD", "pays": {"Français": "Hongrie", "English": "Hungary", "Español": "Hungría"}, "vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ Nuageux - 20°C", "avis": "Magnifique & Pas cher / Great & Cheap"},
        "Porto": {"query": "Porto", "code_iata": "OPO", "pays": {"Français": "Portugal", "English": "Portugal", "Español": "Portugal"}, "vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 Grand soleil - 25°C", "avis": "Parfait pour le soleil / Perfect for sun"},
        "Sofia": {"query": "Sofia", "code_iata": "SOF", "pays": {"Français": "Bulgarie", "English": "Bulgaria", "Español": "Bulgaria"}, "vol": 110, "hotel": 35, "vie": 20, "meteo": "🌤️ Climat agréable - 21°C", "avis": "Une des capitales les moins chères"}
    },
    "Amerique": {
        "New York": {"query": "New York", "code_iata": "NYC", "pays": {"Français": "États-Unis", "English": "USA", "Español": "Estados Unidos"}, "vol": 450, "hotel": 160, "vie": 70, "meteo": "🗽 Ensoleillé - 23°C", "avis": "La métropole mythique américaine"},
        "Montréal": {"query": "Montreal", "code_iata": "YUL", "pays": {"Français": "Canada", "English": "Canada", "Español": "Canadá"}, "vol": 400, "hotel": 110, "vie": 50, "meteo": "🍁 Beau temps - 21°C", "avis": "Une superbe métropole francophone en Amérique"}
    },
    "AsieAfrique": {
        "Marrakech": {"query": "Marrakech", "code_iata": "RAK", "pays": {"Français": "Maroc", "English": "Morocco", "Español": "Marruecos"}, "vol": 120, "hotel": 50, "vie": 25, "meteo": "🌵 Chaud et ensoleillé - 31°C", "avis": "Dépaysement total à petit prix"},
        "Tokyo": {"query": "Tokyo", "code_iata": "TYO", "pays": {"Français": "Japon", "English": "Japan", "Español": "Japón"}, "vol": 750, "hotel": 90, "vie": 45, "meteo": "🌸 Climat idéal - 19°C", "avis": "Un voyage inoubliable mêlant traditions et modernité"},
        "Bangkok": {"query": "Bangkok", "code_iata": "BKK", "pays": {"Français": "Thaïlande", "English": "Thailand", "Español": "Tailandia"}, "vol": 600, "hotel": 30, "vie": 15, "meteo": "🌴 Chaud et tropical - 33°C", "avis": "Une expérience exotique incroyable"}
    }
}

# Fonction réutilisable pour afficher une destination
def afficher_destination(ville, infos, budget, total_voyageurs, nb_jours, str_debut, str_fin, adultes, enfants, lang_booking, code_iata):
    nb_nuits = nb_jours
    cout_vol = infos["vol"] * total_voyageurs
    cout_hotel = infos["hotel"] * nb_nuits * (1 if total_voyageurs <= 2 else 2)
    cout_vie = infos["vie"] * (nb_jours + 1) * total_voyageurs
    total_estime = cout_vol + cout_hotel + cout_vie
    
    if total_estime <= budget:
        reste_a_vivre = budget - total_estime
        nom_pays = f", {infos['pays'][langue]}" if infos['pays'][langue] else ""
        
        st.markdown(f"### 📍 {ville}{nom_pays}")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"- **✈️ {lang['vols']} ({total_voyageurs} pers.)** : {cout_vol}€")
            st.markdown(f"- **🏨 {lang['logement']} ({nb_nuits} nuits)** : {cout_hotel}€")
            st.markdown(f"- **🍔 {lang['vie']} ({nb_jours+1} j.)** : {cout_vie}€")
        with col_c2:
            st.info(f"🌤️ **{lang['meteo']}** : {infos['meteo']}")
            st.metric(label=f"🔥 {lang['reste']}", value=f"{reste_a_vivre}€")
        if infos['avis']:
            st.markdown(f"*{infos['avis']}*")
        
        city_encoded = urllib.parse.quote(infos["query"])
        
        # TRANSFORMATION EN LIENS REDIRECTIONS PROFONDS ET DIRECTS POUR L'AVION ET L'HÔTEL
        link_vol_strict = f"https://tp.st{code_iata}"
        link_hotel_strict = f"https://tp.st{city_encoded}%26checkin%3D{str_debut}%26checkout%3D{str_fin}%26group_adults%3D{adultes}%26group_children%3D{enfants}"
        
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
        dest_test = destination_saisie.strip().lower()
        st.success(lang["success"].format(total=total_voyageurs))
        
        if dest_test:
            cout_vol_unitaire, cout_hotel_nuit, cout_vie_jour = 550, 85, 45
            code_custom = "LON"
            if any(k in dest_test for k in ["paris", "london", "madrid", "barcelona", "rome", "lisbon", "porto", "krakow", "budapest", "sofia", "europe", "pologne", "espagne"]):
                cout_vol_unitaire, cout_hotel_nuit, cout_vie_jour = 80, 40, 25
                code_custom = "KRK" if "kra" in dest_test else "OPO"
            if any(k in dest_test for k in ["marrakech", "maroc", "thailande", "bangkok", "bali", "vietnam"]):
                cout_vol_unitaire = 120 if "mar" in dest_test else 600
                cout_hotel_nuit, cout_vie_jour = 30, 15
                code_custom = "RAK" if "mar" in dest_test else "BKK"
                
            infos_custom = {"query": destination_saisie.strip(), "pays": {"Français": "", "English": "", "Español": ""}, "vol": cout_vol_unitaire, "hotel": cout_hotel_nuit, "vie": cout_vie_jour, "meteo": lang["meteo_txt"], "avis": ""}
            afficher_destination(destination_saisie.strip().capitalize(), infos_custom, budget, total_voyageurs, nb_jours, str_debut, str_fin, adultes, enfants, lang["lang_booking"], code_custom)
        else:
            tab1, tab2, tab3 = st.tabs([lang["tab_eu"], lang["tab_am"], lang["tab_as"]])
            with tab1:
                for v, i in destinations_globales["Europe"].items():
                    afficher_destination(v, i, budget, total_voyageurs, nb_jours, str_debut, str_fin, adultes, enfants, lang["lang_booking"], i["code_iata"])
            with tab2:
                for v, i in destinations_globales["Amerique"].items():
                    afficher_destination(v, i, budget, total_voyageurs, nb_jours, str_debut, str_fin, adultes, enfants, lang["lang_booking"], i["code_iata"])
            with tab3:
                for v, i in destinations_globales["AsieAfrique"].items():
                    afficher_destination(v, i, budget, total_voyageurs, nb_jours, str_debut, str_fin, adultes, enfants, lang["lang_booking"], i["code_iata"])
