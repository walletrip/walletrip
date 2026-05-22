import streamlit as st
import google.generativeai as genai
from datetime import datetime
import urllib.parse

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
            prompt = f"""
            Un utilisateur veut voyager depuis {depart} du {date_debut} au {date_fin} ({nb_jours} nuits).
            Son budget STRICT total pour TOUT le voyage (Vol AR + Hôtel + Vie sur place) est de {budget}€.
            
            Trouve à l'aide de tes connaissances et de tes capacités d'estimation en temps réel pour l'année 2026, 2 ou 3 destinations réelles valides.
            Pour chaque destination, fais le calcul mathématique précis : Vol + (Hôtel par nuit * {nb_jours}) + (Coût de la vie par jour * {nb_jours + 1}).
            Si le total dépasse {budget}€, élimine la destination. Ne montre QUE celles qui entrent dans le budget.
            
            Affiche le résultat au format Markdown suivant pour chaque ville :
            ### 📍 [Nom de la Ville], [Nom du Pays]
            - **✈️ Vol aller-retour estimé** : [Prix]€
            - **🏨 Hébergement ({nb_jours} nuits)** : [Prix total]€
            - **🍔 Vie sur place ({nb_jours + 1} jours)** : [Prix total]€
            - **💰 BUDGET TOTAL ESTIMÉ** : [Somme]€
            - **🔥 VOTRE RESTE-À-VIVRE** : [Calcul du reste]€ d'argent de poche
            - *L'avis de l'IA* : [Explication courte]
            ---
            """
            
            with st.spinner("L'IA calcule le coût de la vie pour vos destinations..."):
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    
                    st.success("Voici les destinations où vous pouvez réellement vous offrir le voyage :")
                    
                    # On affiche le texte de l'IA proprement sans découpage complexe
                    st.markdown(response.text)
                    
                    # BLOC DE LIENS FIXES : Construits sans risque d'erreur directement depuis les saisies
                    st.write("---")
                    st.subheader("🔗 Liens de réservation rapides")
                    st.write("Utilisez ces boutons officiels basés sur vos critères pour réserver vos billets :")
                    
                    # Encodage propre des variables du formulaire
                    dep_enc = urllib.parse.quote(depart)
                    
                    link_vol_global = f"https://skyscanner.fr{dep_enc}/"
                    link_hotel_global = f"https://booking.com{tp_id}&ss=Europe"
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        st.link_button(f"✈️ Comparer les vols au départ de {depart}", link_vol_global)
                    with col_b2:
                        st.link_button("🏨 Trouver un hôtel sur Booking", link_hotel_global)
                        
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de l'appel à l'IA : {e}")
