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
        "warning_no_dest": "Aucune destination mondiale ne correspond à ce budget pour ces dates. Essayez d'augmenter votre budget."
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
        "warning_no_dest": "No worldwide destinations match this budget for these dates. Try increasing your budget."
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
        "warning_no_dest": "Ningún destino mundial coincide con este presupuesto para estas fechas. Intente aumentar su presupuesto."
    }
}

# Sélecteur de langue global
langue = st.selectbox("🌐 Choose Language / Choisir la Langue / Elegir Idioma", ["Français", "English", "Español"])
lang = translations[langue]

st.title(lang["title"])
st.subheader(lang["subtitle"])

# Formulaire utilisateur propre avec la case optionnelle intégrée
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

if submit_button:
    tp_id = "531779"
    total_voyageurs = adultes + enfants
    nb_jours = (date_fin - date_debut).days
    
    if nb_jours <= 0:
        st.error(lang["error_date"])
    else:
        str_debut = date_debut.strftime("%Y-%m-%d")
        str_fin = date_fin.strftime("%Y-%m-%d")
        
        # Catalogue de destinations par défaut du catalogue mondial automatique
        destinations_data = {
            "Cracovie": {"query": "Krakow", "pays": {"Français": "Pologne", "English": "Poland", "Español": "Polonia"}, "vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ Ensoleillé - 22°C", "avis": "Très économique / Highly affordable"},
            "Budapest": {"query": "Budapest", "pays": {"Français": "Hongrie", "English": "Hungary", "Español": "Hungría"}, "vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ Nuageux - 20°C", "avis": "Magnifique & Pas cher / Great & Cheap"},
            "Porto": {"query": "Porto", "pays": {"Français": "Portugal", "English": "Portugal", "Español": "Portugal"}, "vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 Grand soleil - 25°C", "avis": "Parfait pour le soleil / Perfect for sun"},
            "Marrakech": {"query": "Marrakech", "pays": {"Français": "Maroc", "English": "Morocco", "Español": "Marruecos"}, "vol": 120, "hotel": 50, "vie": 25, "meteo": "🌵 Chaud et ensoleillé - 31°C", "avis": "Dépaysement total à petit prix"},
            "Sofia": {"query": "Sofia", "pays": {"Français": "Bulgarie", "English": "Bulgaria", "Español": "Bulgaria"}, "vol": 110, "hotel": 35, "vie": 20, "meteo": "🌤️ Climat agréable - 21°C", "avis": "Une des capitales les moins chères"},
            "New York": {"query": "New York", "pays": {"Français": "États-Unis", "English": "USA", "Español": "Estados Unidos"}, "vol": 450, "hotel": 160, "vie": 70, "meteo": "🗽 Ensoleillé - 23°C", "avis": "La métropole mythique américaine"},
            "Tokyo": {"query": "Tokyo", "pays": {"Français": "Japon", "English": "Japan", "Español": "Japón"}, "vol": 750, "hotel": 90, "vie": 45, "meteo": "🌸 Climat idéal - 19°C", "avis": "Un voyage inoubliable mêlant modernité et traditions"},
            "Bangkok": {"query": "Bangkok", "pays": {"Français": "Thaïlande", "English": "Thailand", "Español": "Tailandia"}, "vol": 600, "hotel": 30, "vie": 15, "meteo": "🌴 Chaud et tropical - 33°C", "avis": "Une expérience exotique incroyable"},
            "Montréal": {"query": "Montreal", "pays": {"Français": "Canada", "English": "Canada", "Español": "Canadá"}, "vol": 400, "hotel": 110, "vie": 50, "meteo": "🍁 Beau temps - 21°C", "avis": "Une superbe métropole francophone en Amérique"}
        }
        
        # Logique intelligente : Filtrer selon la saisie de l'utilisateur si elle existe
        dest_test = destination_saisie.strip().lower()
        
        if dest_test:
            # Si l'utilisateur a écrit une destination mondiale, on calcule une option sur-mesure
            cout_vol_unitaire = 550
            cout_hotel_nuit = 85
            cout_vie_jour = 45
            
            europe_list = ["paris", "london", "londres", "madrid", "barcelona", "barcelone", "rome", "roma", "lisbon", "lisbonne", "porto", "cracovie", "krakow", "budapest", "sofia", "prague", "berlin", "amsterdam", "pologne", "portugal", "espagne", "italie", "hongrie", "bulgarie", "europe"]
            if any(k in dest_test for k in europe_list):
                cout_vol_unitaire, cout_hotel_nuit, cout_vie_jour = 80, 40, 25
                
            low_cost_countries = ["marrakech", "maroc", "morocco", "thailande", "thailand", "bangkok", "bali", "vietnam", "tunisie", "egypte"]
            if any(k in dest_test for k in low_cost_countries):
                cout_vol_unitaire = 120 if "mar" in dest_test else 600
                cout_hotel_nuit, cout_vie_jour = 30, 15
                
            destinations_data = {
                destination_saisie.strip().capitalize(): {
                    "query": destination_saisie.strip(),
                    "pays": {"Français": "", "English": "", "Español": ""},
                    "vol": cout_vol_unitaire,
                    "hotel": cout_hotel_nuit,
                    "vie": cout_vie_jour,
                    "meteo": lang["meteo_txt"],
                    "avis": ""
                }
            }

        st.success(lang["success"].format(total=total_voyageurs))
        valid_destinations = 0
            
        for ville, infos in destinations_data.items():
            cout_vol = infos["vol"] * total_voyageurs
            cout_hotel = infos["hotel"] * nb_jours * (1 if total_voyageurs <= 2 else 2)
            cout_vie = infos["vie"] * (nb_jours + 1) * total_voyageurs
            total_estime = cout_vol + cout_hotel + cout_vie
            
            if total_estime <= budget:
                valid_destinations += 1
                reste_a_vivre = budget - total_estime
                
                nom_pays = f", {infos['pays'][langue]}" if infos['pays'][langue] else ""
                st.markdown(f"### 📍 {ville}{nom_pays}")
                
