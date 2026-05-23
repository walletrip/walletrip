import streamlit as st
import urllib.parse
from datetime import datetime, timedelta

# Configuration de la page Pouch
st.set_page_config(page_title="Pouch", layout="centered")

translations = {
    "Français": {
        "title": "✈️ Pouch",
        "sub": "Trouvez des voyages selon votre budget réel.",
        "dep": "🛫 Départ",
        "dest": "📍 Ville ou Pays précis (Optionnel)",
        "bud": "💰 Budget MAX (€)",
        "d_dep": "🗓️ Date aller",
        "d_ret": "🗓️ Date retour",
        "ad": "👨‍💼 Adultes",
        "ch": "👶 Enfants",
        "btn": "Trouver mon voyage",
        "err": "La date retour doit être après l'aller.",
        "ok": "Options valides pour {total} pers :",
        "v": "Vols",
        "l": "Hôtel",
        "px": "Vie",
        "m": "Météo",
        "r": "RESTE",
        "b_v": "✈️ Rechercher le Vol",
        "b_h": "🏨 Réserver l'Hôtel",
        "t_eu": "🇪🇺 Europe",
        "t_am": "🌎 Amérique",
        "t_as": "🌏 Asie & Afrique"
    }
}

lang = translations["Français"]
st.title(lang["title"])
st.subheader(lang["sub"])

with st.form("budget_form"):
    col1, col2 = st.columns(2)
    with col1:
        depart = st.text_input(lang["dep"], "Paris")
        date_debut = st.date_input(lang["d_dep"], datetime.today())
        adultes = st.number_input(lang["ad"], min_value=1, value=1)
    with col2:
        budget = st.number_input(lang["bud"], min_value=50, value=1500)
        date_fin = st.date_input(lang["d_ret"], datetime.today() + timedelta(days=4))
        enfants = st.number_input(lang["ch"], min_value=0, value=0)
        
    destination_saisie = st.text_input(lang["dest"], "")
    submit_button = st.form_submit_button(label=lang["btn"])

destinations_globales = {
    "Europe": {
        "Cracovie": {"vol": 70, "hotel": 35, "vie": 20, "meteo": "☀️ 22°C", "p": "Pologne", "v": "KRK", "h": "Krakow"},
        "Budapest": {"vol": 85, "hotel": 40, "vie": 25, "meteo": "🌤️ 20°C", "p": "Hongrie", "v": "BUD", "h": "Budapest"},
        "Porto": {"vol": 90, "hotel": 55, "vie": 30, "meteo": "🌊 25°C", "p": "Portugal", "v": "OPO", "h": "Porto"}
    },
    "Amerique": {
        "New York": {"vol": 450, "hotel": 160, "vie": 70, "meteo": "🗽 23°C", "p": "États-Unis", "v": "NYC", "h": "New-York"},
        "Montréal": {"vol": 400, "hotel": 110, "vie": 50, "meteo": "🍁 21°C", "p": "Canada", "v": "YUL", "h": "Montreal"}
    },
    "AsieAfrique": {
        "Marrakech": {"vol": 120, "hotel": 50, "vie": 25, "meteo": "🌵 31°C", "p": "Maroc", "v": "RAK", "h": "Marrakech"},
        "Tokyo": {"vol": 750, "hotel": 90, "vie": 45, "meteo": "🌸 19°C", "p": "Japon", "v": "TYO", "h": "Tokyo"}
    }
}

def afficher_destination(ville, infos):
    cout_v = infos["vol"] * total_voyageurs
    cout_h = infos["hotel"] * nb_jours * (1 if total_voyageurs <= 2 else 2)
    cout_p = infos["vie"] * (nb_jours + 1) * total_voyageurs
    total_estime = cout_v + cout_h + cout_p
    
    if total_estime <= budget:
        reste = budget - total_estime
        st.markdown(f"### 📍 {ville}, {infos['p']}")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"- **{lang['v']}** : {cout_v}€")
            st.markdown(f"- **{lang['l']} ({nb_jours} n.)** : {cout_h}€")
            st.markdown(f"- **{lang['px']}** : {cout_p}€")
        with col_c2:
            st.info(f"🌤️ **{lang['m']}** : {infos['meteo']}")
            st.metric(label=f"🔥 {lang['r']}", value=f"{reste}€")
        
        # SÉCURISATION ABSOLUE DU REFORMATAGE DES ADRESSES WEB (FUSION BLOQUÉE !)
        dep_air = str(depart).strip().upper()
        dest_booking = urllib.parse.quote(infos["h"])
        
        url_aviasales = f"https://aviasales.fr{dep_air}&destination={infos['v']}&depart_date={str_d}&return_date={str_f}"
        url_booking = f"https://booking.com{dest_booking}&checkin={str_d}&checkout={str_f}&group_adults={adultes}&group_children={enfants}"
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.link_button(lang["b_v"], url_aviasales)
        with col_b2:
            st.link_button(lang["b_h"], url_booking)
        st.markdown("---")

if submit_button:
    total_voyageurs = adultes + enfants
    nb_jours = (date_fin - date_debut).days
    
    if nb_jours <= 0:
        st.error(lang["err"])
    else:
        str_d = date_debut.strftime("%Y-%m-%d")
        str_f = date_fin.strftime("%Y-%m-%d")
        dest_test = destination_saisie.strip().lower()
        st.success(lang["ok"].format(total=total_voyageurs))
        
        if dest_test:
            infos_c = {"vol": 500, "hotel": 80, "vie": 40, "meteo": "🌤️ Variable", "p": "", "v": "PAR", "h": destination_saisie.strip()}
            afficher_destination(destination_saisie.strip().capitalize(), infos_c)
        else:
            tab1, tab2, tab3 = st.tabs([lang["t_eu"], lang["t_am"], lang["t_as"]])
            with tab1:
                for v, i in destinations_globales["Europe"].items():
                    afficher_destination(v, i)
            with tab2:
                for v, i in destinations_globales["Amerique"].items():
                    afficher_destination(v, i)
            with tab3:
                for v, i in destinations_globales["AsieAfrique"].items():
                    afficher_destination(v, i)
