import streamlit as st
import urllib.parse
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(page_title="WalletTrip", page_icon="✈️", layout="centered")

# Dictionnaire de traduction automatique pour l'interface mondiale ouverte
translations = {
    "Français": {
        "title": "✈️ WalletTrip",
        "subtitle": "Le comparateur mondial qui calcule votre voyage selon votre budget réel, pas seulement le vol.",
        "depart": "🛫 Ville de départ",
        "destination": "📍 Destination de mes rêves (Ville ou Pays)",
        "budget": "💰 Budget TOTAL maximum (€)",
        "date_dep": "🗓️ Date de départ",
        "date_ret": "🗓️ Date de retour",
        "adults": "👨‍💼 Nombre d'adultes",
        "children": "👶 Nombre d'enfants",
        "button": "Calculer mon budget voyage mondial",
        "error_date": "La date de retour doit être après la date de départ.",
        "error_dest": "Veuillez entrer une destination.",
        "success": "Analyse budgétaire complétée pour {dest} ({total} personnes) :",
        "vols": "Estimation Vols AR",
        "logement": "Estimation Logement",
        "vie": "Estimation Vie sur place",
        "meteo": "Note météo",
        "meteo_txt": "Consultez la météo saisonnière locale avant le départ.",
        "reste": "VOTRE RESTE-À-VIVRE ESTIMÉ",
        "btn_vol": "✈️ Rechercher les vols pour {ville}",
        "btn_hotel": "🏨 Réserver l'hôtel à {ville}",
        "avis_titre": "💡 Note de l'application",
        "avis_txt": "Ce calcul est basé sur les coûts moyens mondiaux de l'année en cours. Utilisez les boutons ci-dessous pour réserver vos tarifs exacts d'affilié.",
        "lang_booking": "fr"
    },
    "English": {
        "title": "✈️ WalletTrip",
        "subtitle": "The global comparator that calculates your trip based on your real budget, not just the flight.",
        "depart": "🛫 Departure City",
        "destination": "📍 Destination of my dreams (City or Country)",
        "budget": "💰 Maximum TOTAL Budget (€)",
        "date_dep": "🗓️ Departure Date",
        "date_ret": "🗓️ Return Date",
        "adults": "👨‍💼 Number of Adults",
        "children": "👶 Number of Children",
        "button": "Calculate my worldwide trip budget",
        "error_date": "Return date must be after departure date.",
        "error_dest": "Please enter a destination.",
        "success": "Budget analysis completed for {dest} ({total} people):",
        "vols": "Estimated Return Flights",
        "logement": "Estimated Accommodation",
        "vie": "Estimated Local Life",
        "meteo": "Weather note",
        "meteo_txt": "Check local seasonal weather before departure.",
        "reste": "YOUR ESTIMATED POCKET MONEY",
        "btn_vol": "✈️ Search flights to {ville}",
        "btn_hotel": "🏨 Book hotel in {ville}",
        "avis_titre": "💡 Application Note",
        "avis_txt": "This calculation is based on current global average costs. Use the buttons below to lock in your exact affiliate rates.",
        "lang_booking": "en-us"
    },
    "Español": {
        "title": "✈️ WalletTrip",
        "subtitle": "El comparador mundial que calcula tu viaje basándose en tu presupuesto real, no solo en el vuelo.",
        "depart": "🛫 Ciudad de salida",
        "destination": "📍 Destino de mis sueños (Ciudad o País)",
        "budget": "💰 Presupuesto TOTAL máximo (€)",
        "date_dep": "Fecha de salida",
        "date_ret": "Fecha de regreso",
        "adults": "👨‍💼 Número de adultos",
        "children": "👶 Número de niños",
        "button": "Calcular mi presupuesto de viaje mundial",
        "error_date": "La fecha de regreso debe ser posterior a la fecha de salida.",
        "error_dest": "Por favor, introduzca un destino.",
        "success": "Análisis de presupuesto completado para {dest} ({total} personas):",
        "vols": "Vuelos AR estimados",
        "logement": "Alojamiento estimado",
        "vie": "Coste de vida estimado",
        "meteo": "Nota del clima",
        "meteo_txt": "Consulte el clima estacional de la zona antes de viajar.",
        "reste": "TU DINERO DE BOLSILLO ESTIMADO",
        "btn_vol": "✈️ Buscar vuelos a {ville}",
        "btn_hotel": "🏨 Reservar hotel en {ville}",
        "avis_titre": "💡 Nota de la aplicación",
        "avis_txt": "Este cálculo se basa en los costes medios globales del año en curso. Utilice los botones de abajo para asegurar sus tarifas exactas de afiliado.",
        "lang_booking": "es"
    }
}

# Sélecteur de langue global
langue = st.selectbox("🌐 Choose Language / Choisir la Langue / Elegir Idioma", ["Français", "English", "Español"])
lang = translations[langue]

st.title(lang["title"])
st.subheader(lang["subtitle"])

# Formulaire utilisateur ouvert sur le monde entier
with st.form("budget_form"):
    depart = st.text_input(lang["depart"], "Paris")
    destination_saisie = st.text_input(lang["destination"], "New York")
    
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input(lang["date_dep"], datetime.today())
        adultes = st.number_input(lang["adults"], min_value=1, value=1, step=1)
    with col2:
        budget = st.number_input(lang["budget"], min_value=50, value=500, step=50)
        date_fin = st.date_input(lang["date_ret"], datetime.today())
        enfants = st.number_input(lang["children"], min_value=0, value=0, step=1)
        
    submit_button = st.form_submit_button(label=lang["button"])

if submit_button:
    total_voyageurs = adultes + enfants
    nb_jours = (date_fin - date_debut).days
    
    if nb_jours <= 0:
        st.error(lang["error_date"])
    elif not destination_saisie.strip():
        st.error(lang["error_dest"])
    else:
        str_debut = date_debut.strftime("%Y-%m-%d")
        str_fin = date_fin.strftime("%Y-%m-%d")
        
        # Algorithme intelligent d'estimation des coûts selon la zone géographique mondiale tapée
        dest_test = destination_saisie.strip().lower()
        
        # Par défaut : Tarifs d'une zone moyenne/long-courrier standard (Ex: Amérique, Asie)
        cout_vol_unitaire = 500
        cout_hotel_nuit = 80
        cout_vie_jour = 40
        
        # Ajustement automatique si c'est une destination européenne proche connue
        europe_keywords = ["paris", "london", "londres", "madrid", "barcelona", "barcelone", "rome", "roma", "lisbon", "lisbonne", "porto", "cracovie", "krakow", "budapest", "sofia", "prague", "berlin", "amsterdam", "bruxelles", "brussels", "pologne", "portugal", "espagne", "italie", "hongrie", "bulgarie"]
        if any(keyword in dest_test for keyword in europe_keywords):
            cout_vol_unitaire = 90
            cout_hotel_nuit = 45
            cout_vie_jour = 25
            
        # Ajustement automatique si c'est une destination asiatique ou maghrébine pas chère (Vol plus cher mais vie très basse)
        asia_maghreb_keywords = ["marrakech", "maroc", "morocco", "tunisie", "tunis", "egypt", "le caire", "bangkok", "thailande", "thailand", "bali", "indonesie", "vietnam", "hanoi", "tokyo", "japon", "japan"]
        if any(keyword in dest_test for keyword in asia_maghreb_keywords):
            cout_vol_unitaire = 450 if "mar" not in dest_test else 120
            cout_hotel_nuit = 35
            cout_vie_jour = 18

        # Calculs proportionnels pour tout le groupe
        cout_vol = cout_vol_unitaire * total_voyageurs
        cout_hotel = cout_hotel_nuit * nb_jours * (1 if total_voyageurs <= 2 else 2)
        cout_vie = cout_vie_jour * (nb_jours + 1) * total_voyageurs
        total_estime = cout_vol + cout_hotel + cout_vie
        reste_a_vivre = budget - total_estime
        
        st.success(lang["success"].format(dest=destination_saisie, total=total_voyageurs))
        st.markdown(f"### 📍 {destination_saisie}")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"- **✈️ {lang['vols']}** : {cout_vol}€")
            st.markdown(f"- **🏨 {lang['logement']} ({nb_jours} nuits)** : {cout_hotel}€")
            st.markdown(f"- **🍔 {lang['vie']} ({nb_jours+1} j.)** : {cout_vie}€")
        with col_c2:
            st.info(f"🌤️ **{lang['meteo']}** : {lang['meteo_txt']}")
            st.metric(label=f"🔥 {lang['reste']}", value=f"{reste_a_vivre}€")
            
        st.warning(f"**{lang['avis_titre']}** : {lang['avis_txt']}")
        
        # Encodage de sécurité de la destination saisie par l'utilisateur
        city_encoded = urllib.parse.quote(destination_saisie.strip())
        
        # LIENS DE REDIRECTION MONDIAUX DIRECTS ET SANS BULLES DE TEXTE CASSÉES
        link_vol_strict = f"https://skyscanner.fr"
        link_hotel_strict = f"https://booking.com{city_encoded}&lang={lang['lang_booking']}&checkin={str_debut}&checkout={str_fin}&group_adults={adultes}&group_children={enfants}"
        
        # Deux boutons de réservation dédiés placés proprement sous la fiche
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.link_button(lang["btn_vol"].format(ville=destination_saisie), link_vol_strict)
        with col_b2:
            st.link_button(lang["btn_hotel"].format(ville=destination_saisie), link_hotel_strict)
        st.markdown("---")
