import streamlit as st
from datetime import datetime

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
    nb_jours = (date_fin - date_debut).days
    
    if nb_jours <= 0:
        st.error("La date de retour doit être après la date de départ.")
    else:
        st.success("Voici les destinations calculées selon vos critères réels :")
        
        # Liste de démonstration fixe et indestructible pour tester
        st.markdown("### 📍 Cracovie, Pologne")
        st.markdown(f"- **✈️ Vol aller-retour estimé** : 70€")
        st.markdown(f"- **🏨 Hébergement ({nb_jours} nuits)** : {40 * nb_jours}€")
        st.markdown(f"- **🍔 Vie sur place ({nb_jours + 1} jours)** : {25 * (nb_jours + 1)}€")
        st.markdown(f"- **🔥 VOTRE RESTE-À-VIVRE CONFLORTABLE**")
        st.markdown("---")
        
        st.markdown("### 📍 Porto, Portugal")
        st.markdown(f"- **✈️ Vol aller-retour estimé** : 80€")
        st.markdown(f"- **🏨 Hébergement ({nb_jours} nuits)** : {65 * nb_jours}€")
        st.markdown(f"- **🍔 Vie sur place ({nb_jours + 1} jours)** : {35 * (nb_jours + 1)}€")
        st.markdown("---")

        # BOUTONS AVEC ADRESSES FIXES ÉCRITES À LA MAIN (IMPOSSIBLE À CORROMPRE)
        st.subheader("🔗 Liens de réservation rapides")
        
        link_vol = "https://skyscanner.fr"
        link_hotel = f"https://booking.com{tp_id}"

        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.link_button("✈️ Ouvrir Skyscanner pour les vols", link_vol)
        with col_b2:
            st.link_button("🏨 Ouvrir Booking pour les hôtels", link_hotel)
