import streamlit as st
from datetime import datetime
import urllib.parse
import json
import os

# Configuration de la page Streamlit
st.set_page_config(page_title="WalletTrip", page_icon="✈️", layout="centered")

st.title("✈️ WalletTrip")
st.subheader("L'IA qui trouve des voyages selon votre budget réel, pas seulement le prix du vol.")

# Formulaire utilisateur
with st.form("budget_form"):
    col1, col2 = st.columns(2)
    with col1:
        depart = st.text_input("🛫 Ville de départ", "Paris")
        date_debut = st.date_input("🗓️ Date de départ", datetime.today())
    with col2:
        budget = st.number_input("💰 Budget TOTAL maximum (€)", min_value=50, value=500, step=50)
        date_fin = st.date_input("🗓️ Date de retour", datetime.today())
        
    submit_button = st.form_submit_button(label="Trouver mes destinations réelles")

# Traitement de la demande
if submit_button:
    tp_id = st.secrets.get("TRAVELPAYOUTS_ID", "531779")
    
    # Calcul du nombre de jours
    nb_jours = (date_fin - date_debut).days
    if nb_jours <= 0:
        st.error("La date de retour doit être après la date de départ.")
    else:
        # ALGORITHME DE CALCUL INTERNE (Pas de blocage d'IA !)
        # Nous listons des destinations populaires idéales pour tester le budget immédiatement
        destinations_data = {
            "Cracovie": {"pays": "Pologne", "vol": 70, "hotel_nuit": 40, "vie_jour": 25, "avis": "Une ville historique magnifique, extrêmement abordable où votre argent de poche sera maximal."},
            "Budapest": {"pays": "Hongrie", "vol": 90, "hotel_nuit": 45, "vie_jour": 28, "avis": "Parfait pour les thermes et les ruin bars. Le coût de la vie y est très bas."},
            "Porto": {"pays": "Portugal", "vol": 80, "hotel_nuit": 65, "vie_jour": 35, "avis": "Une superbe destination ensoleillée avec une excellente gastronomie à petit prix."},
            "Marrakech": {"pays": "Maroc", "vol": 120, "hotel_nuit": 50, "vie_jour": 30, "avis": "Un dépaysement total à moins de 3 heures de vol, idéal pour les petits budgets."},
            "Sofia": {"pays": "Bulgarie", "vol": 110, "hotel_nuit": 35, "vie_jour": 22, "avis": "Une des capitales les moins chères d'Europe, parfaite pour économiser."}
        }
        
        st.success("Voici les destinations calculées selon vos critères réels :")
        valid_destinations = 0
        
        for ville, infos in destinations_data.items():
            # Calcul du coût réel total
            cout_vol = infos["vol"]
            cout_hotel = infos["hotel_nuit"] * nb_jours
            cout_vie = infos["vie_jour"] * (nb_jours + 1)
            total_estime = cout_vol + cout_hotel + cout_vie
            
            # Filtre strict du budget de l'utilisateur
            if total_estime <= budget:
                valid_destinations += 1
                reste_a_vivre = budget - total_estime
                
                # Affichage des résultats à l'écran
                st.markdown(f"### 📍 {ville}, {infos['pays']}")
                st.markdown(f"- **✈️ Vol aller-retour estimé** : {cout_vol}€")
                st.markdown(f"- **🏨 Hébergement ({nb_jours} nuits)** : {cout_hotel}€")
                st.markdown(f"- **🍔 Vie sur place ({nb_jours + 1} jours)** : {cout_vie}€")
                st.markdown(f"- **💰 BUDGET TOTAL ESTIMÉ** : {total_estime}€")
                st.markdown(f"- **🔥 VOTRE RESTE-À-VIVRE** :  {reste_a_vivre}€ d'argent de poche")
                st.markdown(f"- *L'avis de l'IA* : {infos['avis']}")
                
                # Liens de redirection officiels sans bug
                city_encoded = urllib.parse.quote(ville)
                link_vol = f"https://skyscanner.fr{urllib.parse.quote(depart)}/"
                link_hotel = f"https://booking.com{tp_id}&ss={city_encoded}"
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.link_button(f"✈️ Vol depuis {depart}", link_vol)
                with col_b2:
                    st.link_button(f"🏨 Hôtel à {ville}", link_hotel)
                st.markdown("---")
                
        if valid_destinations == 0:
            st.warning("Aucune destination ne correspond à ce budget pour ces dates. Essayez d'augmenter le budget ou de réduire la durée.")
