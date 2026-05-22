import streamlit as st
import google.generativeai as genai
from datetime import datetime
import urllib.parse
import json

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
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Veuillez configurer votre clé API Gemini (GEMINI_API_KEY) dans les paramètres.")
    else:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        tp_id = st.secrets.get("TRAVELPAYOUTS_ID", "531779")
        
        # Calcul du nombre de jours
        nb_jours = (date_fin - date_debut).days
        if nb_jours <= 0:
            st.error("La date de retour doit être après la date de départ.")
        else:
            # On demande à l'IA de répondre sous un format strict de liste JSON que Python sait lire
            prompt = f"""
            Un utilisateur veut voyager depuis {depart} du {date_debut} au {date_fin} ({nb_jours} nuits).
            Son budget STRICT total pour TOUT le voyage (Vol AR + Hôtel + Vie sur place) est de {budget}€.
            
            Trouve 2 ou 3 destinations réelles valides. Le total (Vol + Hôtel + Vie) doit être inférieur à {budget}€.
             Donne ta réponse UNIQUEMENT sous la forme d'un tableau JSON au format suivant, sans autre texte avant ou après :
            [
              {{"ville": "Nom de la ville en anglais", "pays": "Nom du pays", "vol": 70, "hotel": 120, "vie": 90, "reste": 120, "avis": "Explication courte"}}
            ]
            """
            
            with st.spinner("L'IA calcule le coût de la vie et prépare vos liens personnalisés..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    # Nettoyage du texte JSON reçu de l'IA
                    json_text = response.text.strip().replace("```json", "").replace("```", "")
                    destinations = json.loads(json_text)
                    
                    st.success("Voici les destinations où vous pouvez réellement vous offrir le voyage :")
                    
                    # Pour chaque ville trouvée par l'IA, Python génère les explications et les boutons précis !
                    for dest in destinations:
                        st.markdown(f"### 📍 {dest['ville']}, {dest['pays']}")
                        st.markdown(f"- **✈️ Vol aller-retour estimé** : {dest['vol']}€")
                        st.markdown(f"- **🏨 Hébergement ({nb_jours} nuits)** : {dest['hotel']}€")
                        st.markdown(f"- **🍔 Vie sur place ({nb_jours + 1} jours)** : {dest['vie']}€")
                        st.markdown(f"- **🔥 VOTRE RESTE-À-VIVRE** :  {dest['reste']}€ d'argent de poche")
                        st.markdown(f"*L'avis de l'IA* : {dest['avis']}")
                        
                        # Fabrication des liens ultra-précis vers la destination exacte
                        city_encoded = urllib.parse.quote(dest['ville'])
                        dep_encoded = urllib.parse.quote(depart)
                        
                        link_vol = f"https://skyscanner.fr{dep_encoded}/{city_encoded}/"
                        link_hotel = f"https://booking.com{tp_id}&ss={city_encoded}"
                        
                        # Affichage des boutons bleus juste en dessous de la ville concernée
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            st.link_button(f"✈️ Réserver le vol pour {dest['ville']}", link_vol)
                        with col_b2:
                            st.link_button(f"🏨 Trouver un hôtel à {dest['ville']}", link_hotel)
                        st.markdown("---")
                        
                except Exception as e:
                    # En cas de problème de format de l'IA, on affiche quand même son texte brut
                    st.markdown(response.text)
