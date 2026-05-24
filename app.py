"""
Pouch Voyage — Application Streamlit
Travelpayout ID: 731169
"""

import streamlit as st
import requests
import urllib.parse
import math
from datetime import datetime, date, timedelta

# 1. CONFIGURATION DE LA PAGE (CORRIGÉE)
st.set_page_config(
    page_title="Pouch Voyage",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed", # Cache la sidebar pour laisser la place au bandeau
)

# ─────────────────────────────────────────────
#  UNSPLASH PHOTOS PAR DESTINATION
# ─────────────────────────────────────────────
UNSPLASH_PHOTOS = {
    "Tokyo": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600&q=80",
    "Rio de Janeiro": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=600&q=80",
    "Bangkok": "https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=600&q=80",
    "Chiang Mai": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=600&q=80",
    "Malé": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=600&q=80",
    "Lima": "https://images.unsplash.com/photo-1531968455001-5c5272a41129?w=600&q=80",
    "Reykjavik": "https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=600&q=80",
    "Nairobi": "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80",
    "Marrakech": "https://images.unsplash.com/photo-1549144511-f099e773c147?w=600&q=80",
    "New York": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=600&q=80",
    "Bali": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&q=80",
    "Santorin": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=600&q=80",
    "Hanoï": "https://images.unsplash.com/photo-1509030450996-dd1a26dda07a?w=600&q=80",
    "Ho Chi Minh": "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=600&q=80",
    "Kuala Lumpur": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
    "Singapour": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&q=80",
    "Le Cap": "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80",
    "Buenos Aires": "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=600&q=80",
    "Lisbonne": "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=600&q=80",
    "Osaka": "https://images.unsplash.com/photo-1589452271712-64b8a66c7b71?w=600&q=80",
    "Phnom Penh": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=600&q=80",
    "Katmandou": "https://images.unsplash.com/photo-1605640840605-14ac1855827b?w=600&q=80",
}

# ─────────────────────────────────────────────
#  CSS (MIS À JOUR POUR LE BANDEAU HORIZONTAL)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap');
:root {
--cream:#F5F0E8; --cream2:#EDE8DE; --ink:#0D0D0D;
--muted:#6B6560; --border:#D4CFC6; --white:#FEFCF8;
}
html,body,[class*="css"]{font-family:'Inter',sans-serif;background-color:var(--cream)!important;color:var(--ink)!important;}
section[data-testid="stMain"],.main .block-container{background-color:var(--cream)!important; padding-top: 1rem!important;}
header[data-testid="stHeader"]{background:transparent!important;}

/* ── Hero Banner de Luxe ── */
.hero-container {
    position: relative;
    height: 380px;
    background-image: linear-gradient(rgba(13, 13, 13, 0.45), rgba(13, 13, 13, 0.45)), 
                      url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 4.5rem;
    font-weight: 300;
    margin: 0;
    letter-spacing: 0.02em;
    color: #FEFCF8 !important;
    text-shadow: 0 3px 15px rgba(0,0,0,0.4);
}
.hero-slogan {
    font-size: 1.1rem;
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #EDE8DE !important;
    margin-top: 0.5rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
}

/* ── Bandeau de recherche horizontal haut ── */
.top-search-bar {
    background: var(--white);
    border: 1px solid var(--border);
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
}

.dest-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:0.5rem;}
@media(max-width:1100px){.dest-grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:700px){.dest-grid{grid-template-columns:1fr;}}
.dest-card{background:var(--white);border:1px solid var(--border);overflow:hidden;transition:border-color 0.25s,box-shadow 0.25s;position:relative;}
.dest-card:hover{border-color:var(--ink);box-shadow:0 8px 32px rgba(13,13,13,0.10);}
.dest-photo-wrap{position:relative;overflow:hidden;height:190px;}
.dest-photo{width:100%;height:100%;object-fit:cover;transition:transform 0.45s ease, filter 0.45s ease;filter:brightness(0.93);}
.dest-card:hover .dest-photo{transform:scale(1.04);filter:brightness(1.05);}
.fav-ribbon{position:absolute;top:14px;right:-30px;background:var(--ink);color:var(--cream);font-family:'Cormorant Garamond',serif;font-size:0.72rem;font-weight:400;letter-spacing:0.12em;text-transform:uppercase;padding:5px 38px 5px 14px;z-index:10;}
.dest-body{padding:1rem 1.1rem 1.1rem;}
.dest-name{font-family:'Cormorant Garamond',serif;font-size:1.45rem;font-weight:400;color:var(--ink);line-height:1.1;letter-spacing:0.01em;}
.dest-pays{font-size:0.75rem;color:var(--muted);letter-spacing:0.04em;text-transform:uppercase;margin-top:1px;margin-bottom:0.6rem;}
.dest-tags{font-size:0.72rem;color:var(--muted);margin-bottom:0.8rem;letter-spacing:0.02em;}
.dest-price{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;color:var(--ink);line-height:1;letter-spacing:-0.01em;}
.dest-price-label{font-size:0.72rem;color:var(--muted);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.2rem;}
.dest-btns{display:flex;gap:8px;}
.btn-vol{flex:1;background:var(--ink);color:var(--cream);border:1px solid var(--ink);padding:9px 0;text-align:center;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;text-decoration:none;transition:all 0.2s;}
.btn-vol:hover{background:var(--cream);color:var(--ink);}
.btn-hotel{flex:1;background:transparent;color:var(--ink);border:1px solid var(--ink);padding:9px 0;text-align:center;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;text-decoration:none;transition:all 0.2s;}
.btn-hotel:hover{background:var(--ink);color:var(--cream);}
div[data-testid="stVerticalBlockBorderWrapper"]{border:1px solid var(--border)!important;border-radius:0!important;background:var(--white)!important;padding:0.2rem 0.6rem!important;}
div[data-testid="stMetric"]{background:var(--cream2)!important;border:1px solid var(--border)!important;border-radius:0!important;}
div[data-testid="stMetricValue"]{font-family:'Cormorant Garamond',serif!important;font-size:1.8rem!important;color:var(--ink)!important;}
div[data-testid="stButton"] button{background:var(--ink)!important;color:var(--cream)!important;border-radius:0!important;text-transform:uppercase;letter-spacing:0.05em;}
div[data-testid="stButton"] button:hover{background:var(--cream2)!important;color:var(--ink)!important;}
div[data-testid="stSlider"]>div>div>div{background:var(--ink)!important;}
</style>
""", unsafe_allow_html=True)
Travelpayout ID: 731169
"""

import streamlit as st
import requests
import urllib.parse
import math
from datetime import datetime, date, timedelta

st.set_page_config(
    page_title="Pouch Voyage",
    page_icon="✈️",
    layout="wide",
    # ─────────────────────────────────────────────
#  HERO BANNER (Page d'accueil visuelle)
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Pouch Voyage</div>
    <div class="hero-slogan">L'art de voyager selon votre budget</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BANDEAU DE RECHERCHE HORIZONTAL
# ─────────────────────────────────────────────
st.markdown('<div class="top-search-bar">', unsafe_allow_html=True)

# On crée 4 colonnes pour étaler le formulaire horizontalement
col_lang, col_dep, col_dates, col_budget, col_btn = st.columns([1, 1.5, 2, 1.5, 1])

with col_lang:
    lang_key = st.selectbox("Langue", list(LANGS.keys()))
    T = LANGS[lang_key]

with col_dep:
    ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
    ville_idx = st.selectbox(T["depart"], range(len(ville_options)), format_func=lambda i: ville_options[i])
    depart_ville = VILLES_DEPART[ville_idx]
    depart_iata = depart_ville["iata"]

with col_dates:
    st.write(f"<b>{T['dates']}</b>", unsafe_allow_html=True)
    c_d1, c_d2 = st.columns(2)
    with c_d1:
        d1 = st.date_input("Aller", value=date.today() + timedelta(days=30), min_value=date.today(), label_visibility="collapsed")
    with c_d2:
        d2 = st.date_input("Retour", value=date.today() + timedelta(days=60), min_value=date.today(), label_visibility="collapsed")

with col_budget:
    # On affiche le budget avec un slider propre
    budget = st.slider(T["budget"], min_value=500, max_value=15000, value=5000, step=100)

with col_btn:
    st.write("<br>", unsafe_allow_html=True) # Espacement pour aligner le bouton
    chercher = st.button(T["search"], use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Options optionnelles en dessous du bandeau principal si besoin (ex: Voyageurs, Favoris)
with st.expander("🎛️ Options avancées (Voyageurs, Destinations préférées...)"):
    c1, c2, c3, c4 = st.columns(4)
    with c1: adultes = st.number_input(T["adultes"], min_value=1, max_value=9, value=1)
    with c2: enfants = st.number_input(T["enfants"], min_value=0, max_value=9, value=0)
    with c3: bebes = st.number_input(T["bebes"], min_value=0, max_value=9, value=0)
    with c4: fav = st.text_input(T["fav"], placeholder=T["fav_ph"])
    
    nb_stops = st.slider(T["nb_dest"], min_value=2, max_value=8, value=4)
)

# ─────────────────────────────────────────────
#  UNSPLASH PHOTOS PAR DESTINATION
# ─────────────────────────────────────────────
UNSPLASH_PHOTOS = {
    "Tokyo":          "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600&q=80",
    "Rio de Janeiro": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=600&q=80",
    "Bangkok":        "https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=600&q=80",
    "Chiang Mai":     "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=600&q=80",
    "Malé":           "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=600&q=80",
    "Lima":           "https://images.unsplash.com/photo-1531968455001-5c5272a41129?w=600&q=80",
    "Reykjavik":      "https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=600&q=80",
    "Nairobi":        "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=80",
    "Marrakech":      "https://images.unsplash.com/photo-1549144511-f099e773c147?w=600&q=80",
    "New York":       "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=600&q=80",
    "Bali":           "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&q=80",
    "Santorin":       "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=600&q=80",
    "Hanoï":          "https://images.unsplash.com/photo-1509030450996-dd1a26dda07a?w=600&q=80",
    "Ho Chi Minh":    "https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=600&q=80",
    "Kuala Lumpur":   "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?w=600&q=80",
    "Singapour":      "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600&q=80",
    "Le Cap":         "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=600&q=80",
    "Buenos Aires":   "https://images.unsplash.com/photo-1589909202802-8f4aadce1849?w=600&q=80",
    "Lisbonne":       "https://images.unsplash.com/photo-1555881400-74d7acaacd8b?w=600&q=80",
    "Osaka":          "https://images.unsplash.com/photo-1589452271712-64b8a66c7b71?w=600&q=80",
    "Phnom Penh":     "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=600&q=80",
    "Katmandou":      "https://images.unsplash.com/photo-1605640840605-14ac1855827b?w=600&q=80",
}

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap');
  :root {
    --cream:#F5F0E8; --cream2:#EDE8DE; --ink:#0D0D0D;
    --muted:#6B6560; --border:#D4CFC6; --white:#FEFCF8;
  }
  html,body,[class*="css"]{font-family:'Inter',sans-serif;background-color:var(--cream)!important;color:var(--ink)!important;}
  section[data-testid="stMain"],.main .block-container{background-color:var(--cream)!important;}
  section[data-testid="stSidebar"]{background:var(--white)!important;border-right:1px solid var(--border)!important;}
  div[data-testid="stSidebarContent"]{padding:2rem 1.4rem;}
  header[data-testid="stHeader"]{background:var(--cream)!important;}
  .logo-wrap{display:flex;align-items:center;gap:16px;margin:2rem 0 0.4rem;}
  .main-title{font-family:'Cormorant Garamond',serif;font-size:3rem;font-weight:300;color:var(--ink);letter-spacing:0.02em;line-height:1;}
  .subtitle{font-size:0.88rem;font-weight:300;color:var(--muted);margin-bottom:2rem;letter-spacing:0.03em;}
  .summary-box{background:var(--cream2);border:1px solid var(--border);border-radius:0;padding:0.8rem 1.2rem;margin-bottom:2rem;font-size:0.85rem;color:var(--muted);}
  .summary-box b{color:var(--ink);}

  /* ── Grille 3 colonnes ── */
  .dest-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:0.5rem;}
  @media(max-width:1100px){.dest-grid{grid-template-columns:repeat(2,1fr);}}
  @media(max-width:700px){.dest-grid{grid-template-columns:1fr;}}

  /* ── Carte destination ── */
  .dest-card{background:var(--white);border:1px solid var(--border);overflow:hidden;transition:border-color 0.25s,box-shadow 0.25s;position:relative;}
  .dest-card:hover{border-color:var(--ink);box-shadow:0 8px 32px rgba(13,13,13,0.10);}

  /* ── Photo cover ── */
  .dest-photo-wrap{position:relative;overflow:hidden;height:190px;}
  .dest-photo{width:100%;height:100%;object-fit:cover;transition:transform 0.45s ease, filter 0.45s ease;filter:brightness(0.93);}
  .dest-card:hover .dest-photo{transform:scale(1.04);filter:brightness(1.05);}

  /* ── Ruban favori ── */
  .fav-ribbon{position:absolute;top:14px;right:-30px;background:var(--ink);color:var(--cream);font-family:'Cormorant Garamond',serif;font-size:0.72rem;font-weight:400;letter-spacing:0.12em;text-transform:uppercase;padding:5px 38px 5px 14px;transform:rotate(0deg);box-shadow:0 2px 8px rgba(0,0,0,0.18);z-index:10;}

  /* ── Corps de la carte ── */
  .dest-body{padding:1rem 1.1rem 1.1rem;}
  .dest-name{font-family:'Cormorant Garamond',serif;font-size:1.45rem;font-weight:400;color:var(--ink);line-height:1.1;letter-spacing:0.01em;}
  .dest-pays{font-size:0.75rem;color:var(--muted);letter-spacing:0.04em;text-transform:uppercase;margin-top:1px;margin-bottom:0.6rem;}
  .dest-tags{font-size:0.72rem;color:var(--muted);margin-bottom:0.8rem;letter-spacing:0.02em;}

  /* ── Prix magazine ── */
  .dest-price{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;color:var(--ink);line-height:1;letter-spacing:-0.01em;}
  .dest-price-label{font-size:0.72rem;color:var(--muted);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.2rem;}
  .dest-hotel{font-size:0.78rem;color:var(--muted);margin-top:0.25rem;margin-bottom:0.7rem;}
  .dest-reste{font-size:0.78rem;color:var(--muted);background:var(--cream2);border:1px solid var(--border);padding:4px 8px;display:inline-block;margin-bottom:0.85rem;}

  /* ── Boutons ── */
  .dest-btns{display:flex;gap:8px;}
  .btn-vol{flex:1;background:var(--ink);color:var(--cream);border:1px solid var(--ink);padding:9px 0;text-align:center;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;text-decoration:none;font-family:'Inter',sans-serif;transition:background 0.2s,color 0.2s;}
  .btn-vol:hover{background:var(--cream);color:var(--ink);}
  .btn-hotel{flex:1;background:transparent;color:var(--ink);border:1px solid var(--ink);padding:9px 0;text-align:center;font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;text-decoration:none;font-family:'Inter',sans-serif;transition:background 0.2s,color 0.2s;}
  .btn-hotel:hover{background:var(--ink);color:var(--cream);}

  div[data-testid="stVerticalBlockBorderWrapper"]{border:1px solid var(--border)!important;border-radius:0!important;background:var(--white)!important;padding:0.2rem 0.6rem!important;transition:border-color 0.2s!important;}
  div[data-testid="stVerticalBlockBorderWrapper"]:hover{border-color:var(--ink)!important;}
  div[data-testid="stMetric"]{background:var(--cream2)!important;border:1px solid var(--border)!important;border-radius:0!important;padding:0.6rem 1rem!important;}
  div[data-testid="stMetricValue"]{font-family:'Cormorant Garamond',serif!important;font-size:1.8rem!important;font-weight:400!important;color:var(--ink)!important;}
  div[data-testid="stMetricLabel"]{font-size:0.75rem!important;color:var(--muted)!important;}
  div[data-testid="stLinkButton"] a{background:var(--ink)!important;color:var(--cream)!important;border:1px solid var(--ink)!important;border-radius:0!important;font-size:0.78rem!important;font-weight:400!important;letter-spacing:0.06em;text-transform:uppercase;padding:8px 16px!important;}
  div[data-testid="stLinkButton"] a:hover{background:var(--cream)!important;color:var(--ink)!important;}
  div[data-testid="stButton"] button{background:var(--ink)!important;color:var(--cream)!important;border:1px solid var(--ink)!important;border-radius:0!important;font-size:0.8rem!important;font-weight:400!important;letter-spacing:0.06em;text-transform:uppercase;}
  div[data-testid="stButton"] button:hover{background:var(--cream)!important;color:var(--ink)!important;}
  div[data-testid="stSlider"]>div>div>div{background:var(--ink)!important;}
  div[data-testid="stAlert"]{background:var(--cream2)!important;border:1px solid var(--border)!important;border-radius:0!important;color:var(--ink)!important;font-size:0.83rem!important;}
  div[data-testid="stInfo"]{background:var(--cream2)!important;border-color:var(--border)!important;border-radius:0!important;color:var(--muted)!important;}
  .stCaption,[data-testid="stCaptionContainer"] p{color:var(--muted)!important;}
  section[data-testid="stSidebar"] label{color:var(--ink)!important;font-size:0.82rem!important;}
  hr{border-color:var(--border)!important;}
  .no-result{text-align:center;padding:4rem;color:var(--muted);font-size:0.95rem;font-weight:300;}

  /* Itinéraire backpacker */
  .itin-header{font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:300;color:var(--ink);margin:1.5rem 0 0.3rem;letter-spacing:0.02em;}
  .itin-subtitle{font-size:0.82rem;color:var(--muted);margin-bottom:1.5rem;}
  .itin-step{display:flex;gap:1rem;margin-bottom:0;align-items:stretch;}
  .itin-line{display:flex;flex-direction:column;align-items:center;width:28px;flex-shrink:0;}
  .itin-dot{width:10px;height:10px;border-radius:50%;background:var(--ink);flex-shrink:0;margin-top:5px;}
  .itin-dot-home{width:14px;height:14px;border-radius:50%;border:2px solid var(--ink);background:var(--cream);flex-shrink:0;margin-top:3px;}
  .itin-vline{width:1px;background:var(--border);flex:1;margin:4px 0;}
  .itin-content{padding-bottom:1.4rem;flex:1;}
  .itin-city{font-weight:500;font-size:0.95rem;color:var(--ink);}
  .itin-meta{font-size:0.78rem;color:var(--muted);margin-top:2px;}
  .itin-price{font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:var(--ink);margin-top:4px;}
  .itin-tags{font-size:0.72rem;color:var(--muted);margin-top:3px;}
  .budget-bar-wrap{background:var(--cream2);border:1px solid var(--border);padding:1rem 1.2rem;margin:1.5rem 0;}
  .budget-bar-label{font-size:0.78rem;color:var(--muted);margin-bottom:6px;}
  .budget-bar-bg{background:var(--border);height:4px;border-radius:0;}
  .budget-bar-fill{background:var(--ink);height:4px;}
  .budget-numbers{display:flex;justify-content:space-between;margin-top:5px;font-size:0.78rem;color:var(--ink);}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
TRAVELPAYOUT_ID    = "731169"
SKYSCANNER_API_KEY = st.secrets.get("SKYSCANNER_API_KEY", "")
BOOKING_API_KEY    = st.secrets.get("BOOKING_API_KEY", "")
SKYSCANNER_HOST    = "skyscanner50.p.rapidapi.com"
BOOKING_HOST       = "booking-com15.p.rapidapi.com"

# ─────────────────────────────────────────────
#  TRADUCTIONS
# ─────────────────────────────────────────────
LANGS = {
    "🇫🇷 Français": {
        "subtitle":"Trouvez votre prochaine aventure selon votre budget",
        "tab_dest":"Destinations","tab_back":"Backpacker",
        "depart":"Ville de départ","dates":"Dates du voyage",
        "budget":"Budget total (€)","budget_sel":"Budget : {b:,} €",
        "voyageurs":"Voyageurs","adultes":"Adultes","enfants":"Enfants","bebes":"Bébés",
        "nb_dest":"Nombre de destinations (backpacker)","duree_label":"durée",
        "fav":"Destination préférée (optionnel)","fav_ph":"ex : Tokyo, Bali…",
        "search":"Rechercher","powered":"Propulsé par Travelpayout",
        "fill_form":"Remplissez le formulaire et cliquez sur Rechercher.",
        "date_err":"La date de retour doit être après la date de départ.",
        "found":"{n} destination(s) · {nuits} nuit(s) · {v} voyageur(s) · Budget {b:,} €",
        "no_result":"Aucune destination dans ce budget. Essayez d'augmenter le budget.",
        "price_live":"Vol (prix en direct)","price_est":"Prix de départ estimé",
        "price_help":"Indicatif — cliquez Skyscanner pour le prix exact.",
        "hotel_live":"Hôtel : ~{p:,} €/nuit","reste":"Budget restant : {r:,} € — {n} nuits",
        "btn_sky":"✈ Vol","btn_book":"🏨 Hôtel","fav_label":"Favori",
        "back_title":"Votre circuit backpacker","back_sub":"Itinéraire optimisé · {n} étapes · {nuits} nuits au total",
        "back_depart":"Départ","back_retour":"Retour",
        "back_nuits":"{n} nuits","back_vol":"Vol estimé","back_hotel":"Hôtel ~{p} €/nuit",
        "back_budget_used":"Budget utilisé","back_budget_rest":"Reste",
        "back_no":"Pas assez de destinations dans ce budget pour un circuit backpacker.",
        "back_btn_sky":"Réserver ce vol","back_btn_book":"Trouver un hôtel",
        "nuits_label":"nuits par étape",
        "tab_meteo":"Météo","tab_cout":"Coût de la vie",
        "city_ph":"ex: Tokyo, Bangkok, Lisbonne…",
        "cout_title":"Coût de la vie à {city}","cout_sub":"Budget estimé par personne et par jour",
        "cout_total":"Total / jour","cout_repas":"🍽 Repas",
        "cout_transport":"🚌 Transport","cout_logement":"🏨 Logement",
        "cout_loisirs":"🎭 Loisirs","cout_jour":"€/jour",
        "cout_notfound":"Ville introuvable dans notre base. Essayez un autre nom.",
        "meteo_title":"Météo actuelle à {city}","meteo_notfound":"Impossible de récupérer la météo. Vérifiez le nom de la ville.",
        "meteo_feels":"Ressenti {f}°C","meteo_hum":"Humidité {h}%",
        "meteo_wind":"Vent {w} km/h","meteo_minmax":"Min {mn}° / Max {mx}°",
        "meteo_sun":"🌅 {sr}  🌇 {ss}",
    },
    "🇬🇧 English": {
        "subtitle":"Find your next adventure within your budget",
        "tab_dest":"Destinations","tab_back":"Backpacker",
        "depart":"Departure city","dates":"Travel dates",
        "budget":"Total budget (€)","budget_sel":"Budget: €{b:,}",
        "voyageurs":"Travellers","adultes":"Adults","enfants":"Children","bebes":"Infants",
        "nb_dest":"Number of stops (backpacker)","duree_label":"duration",
        "fav":"Preferred destination (optional)","fav_ph":"e.g. Tokyo, Bali…",
        "search":"Search","powered":"Powered by Travelpayout",
        "fill_form":"Fill in the form and click Search.",
        "date_err":"Return date must be after departure date.",
        "found":"{n} destination(s) · {nuits} night(s) · {v} traveller(s) · Budget €{b:,}",
        "no_result":"No destinations in this budget. Try increasing it.",
        "price_live":"Flight (live price)","price_est":"Estimated price",
        "price_help":"Indicative — click Skyscanner for exact price.",
        "hotel_live":"Hotel: ~€{p:,}/night","reste":"Remaining: €{r:,} — {n} nights",
        "btn_sky":"✈ Flight","btn_book":"🏨 Hotel","fav_label":"Favourite",
        "back_title":"Your backpacker route","back_sub":"Optimised itinerary · {n} stops · {nuits} nights total",
        "back_depart":"Departure","back_retour":"Return",
        "back_nuits":"{n} nights","back_vol":"Est. flight","back_hotel":"Hotel ~€{p}/night",
        "back_budget_used":"Budget used","back_budget_rest":"Remaining",
        "back_no":"Not enough destinations in this budget for a backpacker route.",
        "back_btn_sky":"Book this flight","back_btn_book":"Find a hotel",
        "nuits_label":"nights per stop",
        "tab_meteo":"Weather","tab_cout":"Cost of living",
        "city_ph":"e.g. Tokyo, Bangkok, Lisbon…",
        "cout_title":"Cost of living in {city}","cout_sub":"Estimated budget per person per day",
        "cout_total":"Total / day","cout_repas":"🍽 Meals",
        "cout_transport":"🚌 Transport","cout_logement":"🏨 Accommodation",
        "cout_loisirs":"🎭 Activities","cout_jour":"€/day",
        "cout_notfound":"City not found. Try another name.",
        "meteo_title":"Current weather in {city}","meteo_notfound":"Unable to fetch weather. Check the city name.",
        "meteo_feels":"Feels like {f}°C","meteo_hum":"Humidity {h}%",
        "meteo_wind":"Wind {w} km/h","meteo_minmax":"Min {mn}° / Max {mx}°",
        "meteo_sun":"🌅 {sr}  🌇 {ss}",
    },
    "🇪🇸 Español": {
        "subtitle":"Encuentra tu próxima aventura según tu presupuesto",
        "tab_dest":"Destinos","tab_back":"Mochilero",
        "depart":"Ciudad de salida","dates":"Fechas del viaje",
        "budget":"Presupuesto total (€)","budget_sel":"Presupuesto: {b:,} €",
        "voyageurs":"Viajeros","adultes":"Adultos","enfants":"Niños","bebes":"Bebés",
        "nb_dest":"Número de destinos (mochilero)","duree_label":"duración",
        "fav":"Destino preferido (opcional)","fav_ph":"ej: Tokio, Bali…",
        "search":"Buscar","powered":"Desarrollado por Travelpayout",
        "fill_form":"Rellena el formulario y haz clic en Buscar.",
        "date_err":"La fecha de regreso debe ser posterior a la de salida.",
        "found":"{n} destino(s) · {nuits} noche(s) · {v} viajero(s) · Presupuesto {b:,} €",
        "no_result":"Ningún destino en este presupuesto. Intenta aumentarlo.",
        "price_live":"Vuelo (precio en directo)","price_est":"Precio estimado",
        "price_help":"Indicativo — haz clic en Skyscanner para el precio exacto.",
        "hotel_live":"Hotel: ~{p:,} €/noche","reste":"Restante: {r:,} € — {n} noches",
        "btn_sky":"✈ Vuelo","btn_book":"🏨 Hotel","fav_label":"Favorito",
        "back_title":"Tu ruta mochilera","back_sub":"Itinerario optimizado · {n} paradas · {nuits} noches en total",
        "back_depart":"Salida","back_retour":"Regreso",
        "back_nuits":"{n} noches","back_vol":"Vuelo estimado","back_hotel":"Hotel ~{p} €/noche",
        "back_budget_used":"Presupuesto usado","back_budget_rest":"Restante",
        "back_no":"No hay suficientes destinos en este presupuesto para una ruta mochilera.",
        "back_btn_sky":"Reservar este vuelo","back_btn_book":"Buscar hotel",
        "nuits_label":"noches por etapa",
        "tab_meteo":"Meteorología","tab_cout":"Coste de la vida",
        "city_ph":"ej: Tokio, Bangkok, Lisboa…",
        "cout_title":"Coste de la vida en {city}","cout_sub":"Presupuesto estimado por persona y día",
        "cout_total":"Total / día","cout_repas":"🍽 Comidas",
        "cout_transport":"🚌 Transporte","cout_logement":"🏨 Alojamiento",
        "cout_loisirs":"🎭 Actividades","cout_jour":"€/día",
        "cout_notfound":"Ciudad no encontrada. Prueba otro nombre.",
        "meteo_title":"Tiempo actual en {city}","meteo_notfound":"No se puede obtener el tiempo. Verifica el nombre.",
        "meteo_feels":"Sensación {f}°C","meteo_hum":"Humedad {h}%",
        "meteo_wind":"Viento {w} km/h","meteo_minmax":"Mín {mn}° / Máx {mx}°",
        "meteo_sun":"🌅 {sr}  🌇 {ss}",
    },
}

# ─────────────────────────────────────────────
#  DONNÉES
# ─────────────────────────────────────────────
VILLES_DEPART = [
    {"nom":"Paris",    "pays":"France",    "flag":"🇫🇷","iata":"CDG","lat":48.85,"lng":2.35},
    {"nom":"Lyon",     "pays":"France",    "flag":"🇫🇷","iata":"LYS","lat":45.75,"lng":4.83},
    {"nom":"Marseille","pays":"France",    "flag":"🇫🇷","iata":"MRS","lat":43.30,"lng":5.38},
    {"nom":"Bruxelles","pays":"Belgique",  "flag":"🇧🇪","iata":"BRU","lat":50.85,"lng":4.35},
    {"nom":"Genève",   "pays":"Suisse",    "flag":"🇨🇭","iata":"GVA","lat":46.20,"lng":6.14},
    {"nom":"Montréal", "pays":"Canada",    "flag":"🇨🇦","iata":"YUL","lat":45.50,"lng":-73.57},
    {"nom":"Phuket",   "pays":"Thaïlande", "flag":"🇹🇭","iata":"HKT","lat":7.88,"lng":98.39},
]

DESTINATIONS = [
    {"flag":"🇯🇵","nom":"Tokyo",         "pays":"Japon",         "iata":"TYO","booking_id":"Tokyo",        "tags":["Culture","Gastronomie","Modernité"], "prix_base":2200,"lat":35.68,"lng":139.69,"region":"Asie"},
    {"flag":"🇧🇷","nom":"Rio de Janeiro","pays":"Brésil",        "iata":"GIG","booking_id":"Rio de Janeiro","tags":["Plage","Fête","Nature"],             "prix_base":1800,"lat":-22.90,"lng":-43.17,"region":"Amérique du Sud"},
    {"flag":"🇹🇭","nom":"Bangkok",       "pays":"Thaïlande",     "iata":"BKK","booking_id":"Bangkok",       "tags":["Street food","Temples","Nuit"],      "prix_base":800, "lat":13.75,"lng":100.50,"region":"Asie du Sud-Est"},
    {"flag":"🇹🇭","nom":"Chiang Mai",    "pays":"Thaïlande",     "iata":"CNX","booking_id":"Chiang Mai",   "tags":["Temples","Nature","Détente"],        "prix_base":950, "lat":18.79,"lng":98.98,"region":"Asie du Sud-Est"},
    {"flag":"🇲🇻","nom":"Malé",          "pays":"Maldives",      "iata":"MLE","booking_id":"Male",         "tags":["Luxe","Plage","Snorkeling"],         "prix_base":4500,"lat":4.17,"lng":73.51,"region":"Océan Indien"},
    {"flag":"🇵🇪","nom":"Lima",          "pays":"Pérou",         "iata":"LIM","booking_id":"Lima",         "tags":["Gastronomie","Histoire","Surf"],      "prix_base":1800,"lat":-12.05,"lng":-77.04,"region":"Amérique du Sud"},
    {"flag":"🇮🇸","nom":"Reykjavik",     "pays":"Islande",       "iata":"KEF","booking_id":"Reykjavik",    "tags":["Aurores","Nature","Volcans"],        "prix_base":2100,"lat":64.13,"lng":-21.82,"region":"Europe Nord"},
    {"flag":"🇰🇪","nom":"Nairobi",       "pays":"Kenya",         "iata":"NBO","booking_id":"Nairobi",      "tags":["Safari","Faune","Savane"],           "prix_base":3200,"lat":-1.29,"lng":36.82,"region":"Afrique"},
    {"flag":"🇲🇦","nom":"Marrakech",     "pays":"Maroc",         "iata":"RAK","booking_id":"Marrakech",    "tags":["Souk","Culture","Désert"],           "prix_base":800, "lat":31.63,"lng":-7.99,"region":"Afrique du Nord"},
    {"flag":"🇺🇸","nom":"New York",      "pays":"États-Unis",    "iata":"JFK","booking_id":"New York City","tags":["Ville","Shopping","Culture"],        "prix_base":2900,"lat":40.71,"lng":-74.00,"region":"Amérique du Nord"},
    {"flag":"🇮🇩","nom":"Bali",          "pays":"Indonésie",     "iata":"DPS","booking_id":"Bali",         "tags":["Spiritualité","Plage","Jungle"],     "prix_base":1400,"lat":-8.34,"lng":115.09,"region":"Asie du Sud-Est"},
    {"flag":"🇬🇷","nom":"Santorin",      "pays":"Grèce",         "iata":"JTR","booking_id":"Santorini",    "tags":["Romance","Mer","Gastronomie"],       "prix_base":1600,"lat":36.39,"lng":25.46,"region":"Europe Sud"},
    {"flag":"🇻🇳","nom":"Hanoï",         "pays":"Vietnam",       "iata":"HAN","booking_id":"Hanoi",        "tags":["Rue","Histoire","Gastronomie"],      "prix_base":900, "lat":21.03,"lng":105.85,"region":"Asie du Sud-Est"},
    {"flag":"🇻🇳","nom":"Ho Chi Minh",   "pays":"Vietnam",       "iata":"SGN","booking_id":"Ho Chi Minh City","tags":["Énergie","Gastronomie","Histoire"],"prix_base":850,"lat":10.82,"lng":106.63,"region":"Asie du Sud-Est"},
    {"flag":"🇲🇾","nom":"Kuala Lumpur",  "pays":"Malaisie",      "iata":"KUL","booking_id":"Kuala Lumpur", "tags":["Moderne","Street food","Shopping"],  "prix_base":750, "lat":3.14,"lng":101.69,"region":"Asie du Sud-Est"},
    {"flag":"🇸🇬","nom":"Singapour",     "pays":"Singapour",     "iata":"SIN","booking_id":"Singapore",    "tags":["Luxe","Gastronomie","Modernité"],    "prix_base":1000,"lat":1.35,"lng":103.82,"region":"Asie du Sud-Est"},
    {"flag":"🇿🇦","nom":"Le Cap",        "pays":"Afrique du Sud","iata":"CPT","booking_id":"Cape Town",    "tags":["Nature","Vignobles","Mer"],          "prix_base":2400,"lat":-33.93,"lng":18.42,"region":"Afrique"},
    {"flag":"🇦🇷","nom":"Buenos Aires",  "pays":"Argentine",     "iata":"EZE","booking_id":"Buenos Aires", "tags":["Tango","Gastronomie","Culture"],     "prix_base":2000,"lat":-34.61,"lng":-58.38,"region":"Amérique du Sud"},
    {"flag":"🇵🇹","nom":"Lisbonne",      "pays":"Portugal",      "iata":"LIS","booking_id":"Lisbon",       "tags":["Histoire","Fado","Gastronomie"],     "prix_base":700, "lat":38.72,"lng":-9.14,"region":"Europe"},
    {"flag":"🇯🇵","nom":"Osaka",         "pays":"Japon",         "iata":"KIX","booking_id":"Osaka",        "tags":["Street food","Modernité","Culture"],  "prix_base":2000,"lat":34.69,"lng":135.50,"region":"Asie"},
    {"flag":"🇨🇲","nom":"Phnom Penh",    "pays":"Cambodge",      "iata":"PNH","booking_id":"Phnom Penh",   "tags":["Histoire","Temples","Fleuve"],       "prix_base":750, "lat":11.56,"lng":104.92,"region":"Asie du Sud-Est"},
    {"flag":"🇳🇵","nom":"Katmandou",     "pays":"Népal",         "iata":"KTM","booking_id":"Kathmandu",    "tags":["Himalaya","Trek","Spiritualité"],    "prix_base":1100,"lat":27.70,"lng":85.31,"region":"Asie du Sud"},
]

# ─────────────────────────────────────────────
#  UTILITAIRES
# ─────────────────────────────────────────────
def prix_total(prix_base, adultes, enfants, bebes):
    return round(prix_base * adultes + prix_base * 0.70 * enfants + prix_base * 0.10 * bebes)

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def build_skyscanner_url(orig, dest, d1, d2, adultes, enfants, bebes):
    fmt = lambda d: d.replace("-","")
    return (
        f"https://www.skyscanner.fr/transport/vols/{orig.lower()}/{dest.lower()}/{fmt(d1)}/{fmt(d2)}/"
        f"?adults={adultes}&children={enfants}&infants={bebes}"
        f"&utm_source=travelpayout&utm_medium=affiliate&utm_campaign={TRAVELPAYOUT_ID}"
    )

def build_booking_url(destination, d1, d2, adultes, enfants):
    booking_aid = st.secrets.get("BOOKING_AID","")
    aid_param = f"&aid={booking_aid}" if booking_aid else ""
    dest_enc = urllib.parse.quote(destination)
    return (
        f"https://www.booking.com/searchresults.fr.html"
        f"?ss={dest_enc}&checkin={d1}&checkout={d2}"
        f"&group_adults={adultes}&group_children={enfants}&no_rooms=1{aid_param}"
    )

@st.cache_data(ttl=300, show_spinner=False)
def get_skyscanner_prices(orig_iata, dest_iata, d1, d2, adultes):
    if not SKYSCANNER_API_KEY: return None
    url = f"https://{SKYSCANNER_HOST}/api/v1/flights/searchFlights"
    headers = {"X-RapidAPI-Key":SKYSCANNER_API_KEY,"X-RapidAPI-Host":SKYSCANNER_HOST}
    params = {"originSkyId":orig_iata,"destinationSkyId":dest_iata,"originEntityId":orig_iata,
              "destinationEntityId":dest_iata,"date":d1,"returnDate":d2,"adults":adultes,
              "currency":"EUR","locale":"fr-FR","market":"FR","countryCode":"FR","cabinClass":"economy"}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        itin = resp.json().get("data",{}).get("itineraries",{}).get("results",[])
        if itin:
            prices = [it["price"]["raw"] for it in itin if it.get("price",{}).get("raw")]
            if prices: return {"price":round(min(prices))}
    except: pass
    return None

@st.cache_data(ttl=300, show_spinner=False)
def get_booking_hotel_price(destination, d1, d2, adultes, nuits):
    if not BOOKING_API_KEY: return None
    headers = {"X-RapidAPI-Key":BOOKING_API_KEY,"X-RapidAPI-Host":BOOKING_HOST}
    try:
        r1 = requests.get(f"https://{BOOKING_HOST}/api/v1/hotels/searchDestination",
                          headers=headers, params={"query":destination}, timeout=6)
        r1.raise_for_status()
        results = r1.json().get("data",[])
        if not results: return None
        dest_id, dest_type = results[0]["dest_id"], results[0]["dest_type"]
        r2 = requests.get(f"https://{BOOKING_HOST}/api/v1/hotels/searchHotels", headers=headers,
                          params={"dest_id":dest_id,"search_type":dest_type,"arrival_date":d1,
                                  "departure_date":d2,"adults":adultes,"room_qty":1,
                                  "currency_code":"EUR","languagecode":"fr","sort_by":"popularity"}, timeout=8)
        r2.raise_for_status()
        hotels = r2.json().get("data",{}).get("hotels",[])
        if hotels:
            prices = [h["property"]["priceBreakdown"]["grossPrice"]["value"]
                      for h in hotels[:10]
                      if h.get("property",{}).get("priceBreakdown",{}).get("grossPrice",{}).get("value")]
            if prices: return {"price_per_night":round(sum(prices)/len(prices)/nuits)}
    except: pass
    return None

# ─────────────────────────────────────────────
#  MÉTÉO
# ─────────────────────────────────────────────
WX_CODES = {
    0:("Ciel dégagé","☀️"), 1:("Principalement clair","🌤"), 2:("Partiellement nuageux","⛅"),
    3:("Couvert","☁️"), 45:("Brouillard","🌫"), 48:("Brouillard givrant","🌫"),
    51:("Bruine légère","🌦"), 53:("Bruine modérée","🌦"), 55:("Bruine dense","🌧"),
    61:("Pluie légère","🌧"), 63:("Pluie modérée","🌧"), 65:("Pluie forte","🌧"),
    71:("Neige légère","🌨"), 73:("Neige modérée","🌨"), 75:("Neige forte","❄️"),
    80:("Averses légères","🌦"), 81:("Averses modérées","🌧"), 82:("Averses fortes","⛈"),
    95:("Orage","⛈"), 96:("Orage avec grêle","⛈"), 99:("Orage violent","⛈"),
}

@st.cache_data(ttl=600, show_spinner=False)
def get_weather(city: str):
    try:
        geo = requests.get("https://nominatim.openstreetmap.org/search",
            params={"q":city,"format":"json","limit":1},
            headers={"User-Agent":"PouchVoyage/1.0"}, timeout=6).json()
        if not geo: return None
        lat  = float(geo[0]["lat"])
        lon  = float(geo[0]["lon"])
        name = geo[0].get("display_name", city).split(",")[0]
        wx = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude":lat,"longitude":lon,
            "current":"temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
            "daily":"sunrise,sunset,temperature_2m_max,temperature_2m_min",
            "timezone":"auto","forecast_days":1}, timeout=6).json()
        cur   = wx.get("current",{})
        daily = wx.get("daily",{})
        code  = cur.get("weather_code",0)
        desc, emoji = WX_CODES.get(code,("—","🌡"))
        fmt_time = lambda s: s.split("T")[1][:5] if "T" in s else s
        return {
            "city":name, "temp":round(cur.get("temperature_2m",0)),
            "feels":round(cur.get("apparent_temperature",0)),
            "humidity":cur.get("relative_humidity_2m",0),
            "wind":round(cur.get("wind_speed_10m",0)),
            "desc":desc, "emoji":emoji, "is_day":cur.get("is_day",1),
            "temp_max":round(daily.get("temperature_2m_max",[0])[0]),
            "temp_min":round(daily.get("temperature_2m_min",[0])[0]),
            "sunrise":fmt_time(daily.get("sunrise",[""])[0]),
            "sunset":fmt_time(daily.get("sunset",[""])[0]),
        }
    except: return None

# ─────────────────────────────────────────────
#  COÛT DE LA VIE
# ─────────────────────────────────────────────
COST_DB = {
    "bangkok":{"repas":12,"transport":4,"logement":25,"loisirs":10},
    "chiang mai":{"repas":10,"transport":3,"logement":20,"loisirs":8},
    "bali":{"repas":14,"transport":5,"logement":35,"loisirs":12},
    "tokyo":{"repas":28,"transport":10,"logement":80,"loisirs":20},
    "kyoto":{"repas":25,"transport":8,"logement":70,"loisirs":18},
    "osaka":{"repas":22,"transport":8,"logement":65,"loisirs":16},
    "séoul":{"repas":18,"transport":5,"logement":55,"loisirs":15},
    "seoul":{"repas":18,"transport":5,"logement":55,"loisirs":15},
    "hanoï":{"repas":8,"transport":3,"logement":20,"loisirs":7},
    "hanoi":{"repas":8,"transport":3,"logement":20,"loisirs":7},
    "ho chi minh":{"repas":9,"transport":3,"logement":22,"loisirs":8},
    "singapour":{"repas":22,"transport":8,"logement":90,"loisirs":20},
    "singapore":{"repas":22,"transport":8,"logement":90,"loisirs":20},
    "kuala lumpur":{"repas":12,"transport":4,"logement":30,"loisirs":10},
    "male":{"repas":30,"transport":15,"logement":150,"loisirs":25},
    "malé":{"repas":30,"transport":15,"logement":150,"loisirs":25},
    "kathmandu":{"repas":8,"transport":2,"logement":15,"loisirs":6},
    "phuket":{"repas":15,"transport":6,"logement":40,"loisirs":12},
    "ubud":{"repas":12,"transport":5,"logement":30,"loisirs":10},
    "paris":{"repas":35,"transport":10,"logement":100,"loisirs":25},
    "lisbonne":{"repas":22,"transport":6,"logement":60,"loisirs":18},
    "lisbon":{"repas":22,"transport":6,"logement":60,"loisirs":18},
    "barcelone":{"repas":28,"transport":8,"logement":75,"loisirs":20},
    "barcelona":{"repas":28,"transport":8,"logement":75,"loisirs":20},
    "madrid":{"repas":26,"transport":7,"logement":70,"loisirs":18},
    "rome":{"repas":30,"transport":8,"logement":80,"loisirs":20},
    "amsterdam":{"repas":32,"transport":9,"logement":90,"loisirs":22},
    "berlin":{"repas":25,"transport":7,"logement":65,"loisirs":18},
    "prague":{"repas":18,"transport":5,"logement":45,"loisirs":14},
    "budapest":{"repas":16,"transport":4,"logement":40,"loisirs":12},
    "athènes":{"repas":22,"transport":5,"logement":55,"loisirs":15},
    "athens":{"repas":22,"transport":5,"logement":55,"loisirs":15},
    "santorin":{"repas":35,"transport":8,"logement":120,"loisirs":25},
    "santorini":{"repas":35,"transport":8,"logement":120,"loisirs":25},
    "reykjavik":{"repas":50,"transport":15,"logement":120,"loisirs":30},
    "stockholm":{"repas":40,"transport":12,"logement":100,"loisirs":25},
    "copenhague":{"repas":45,"transport":12,"logement":110,"loisirs":28},
    "copenhagen":{"repas":45,"transport":12,"logement":110,"loisirs":28},
    "vienne":{"repas":30,"transport":9,"logement":80,"loisirs":20},
    "vienna":{"repas":30,"transport":9,"logement":80,"loisirs":20},
    "bruxelles":{"repas":28,"transport":8,"logement":80,"loisirs":20},
    "brussels":{"repas":28,"transport":8,"logement":80,"loisirs":20},
    "genève":{"repas":55,"transport":15,"logement":130,"loisirs":35},
    "geneva":{"repas":55,"transport":15,"logement":130,"loisirs":35},
    "zurich":{"repas":60,"transport":16,"logement":140,"loisirs":38},
    "marrakech":{"repas":14,"transport":4,"logement":35,"loisirs":10},
    "new york":{"repas":45,"transport":12,"logement":150,"loisirs":30},
    "new york city":{"repas":45,"transport":12,"logement":150,"loisirs":30},
    "los angeles":{"repas":40,"transport":15,"logement":130,"loisirs":28},
    "miami":{"repas":38,"transport":14,"logement":120,"loisirs":26},
    "montréal":{"repas":30,"transport":8,"logement":80,"loisirs":20},
    "montreal":{"repas":30,"transport":8,"logement":80,"loisirs":20},
    "buenos aires":{"repas":12,"transport":3,"logement":30,"loisirs":8},
    "rio de janeiro":{"repas":18,"transport":5,"logement":50,"loisirs":12},
    "nairobi":{"repas":16,"transport":5,"logement":40,"loisirs":10},
    "le cap":{"repas":18,"transport":6,"logement":45,"loisirs":12},
    "cape town":{"repas":18,"transport":6,"logement":45,"loisirs":12},
    "dubaï":{"repas":35,"transport":12,"logement":110,"loisirs":28},
    "dubai":{"repas":35,"transport":12,"logement":110,"loisirs":28},
    "istanbul":{"repas":16,"transport":4,"logement":40,"loisirs":12},
    "sydney":{"repas":40,"transport":10,"logement":110,"loisirs":28},
    "queenstown":{"repas":35,"transport":10,"logement":90,"loisirs":22},
    "phnom penh":{"repas":8,"transport":3,"logement":18,"loisirs":6},
    "katmandou":{"repas":8,"transport":2,"logement":15,"loisirs":6},
    "lima":{"repas":14,"transport":4,"logement":32,"loisirs":9},
}

def get_cost_of_living(city: str):
    key = city.lower().strip()
    if key in COST_DB:
        return COST_DB[key]
    try:
        url = f"https://www.numbeo.com/api/city_prices?api_key=free&query={urllib.parse.quote(city)}&currency=EUR"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            items = {item["item_id"]: item["average_price"] for item in data.get("prices",[])}
            if items:
                repas     = round((items.get(1,0)+items.get(2,0))/2)
                transport = round(items.get(20,0)*2)
                logement  = round(items.get(26,0)/30)
                loisirs   = round(items.get(44,0)+items.get(28,0))
                if repas > 0:
                    return {"repas":repas,"transport":transport or 5,"logement":logement or 40,"loisirs":loisirs or 12}
    except: pass
    return None

def build_backpacker_route(depart_ville, nb_stops, budget_total, adultes, enfants, bebes, nuits_par_etape):
    lat0, lng0 = depart_ville["lat"], depart_ville["lng"]
    budget_par_etape = budget_total / (nb_stops + 1)
    candidats = []
    for d in DESTINATIONS:
        prix = prix_total(d["prix_base"], adultes, enfants, bebes)
        if prix <= budget_par_etape * 2.5:
            dist = haversine(lat0, lng0, d["lat"], d["lng"])
            candidats.append({**d, "prix_estime": prix, "dist_depart": dist})
    if len(candidats) < nb_stops:
        return []
    route = []
    restants = candidats.copy()
    cur_lat, cur_lng = lat0, lng0
    for _ in range(nb_stops):
        if not restants: break
        restants.sort(key=lambda x: haversine(cur_lat, cur_lng, x["lat"], x["lng"]))
        pool = restants[:max(3, len(restants)//3)]
        pool.sort(key=lambda x: x["prix_estime"])
        choix = pool[0]
        route.append(choix)
        cur_lat, cur_lng = choix["lat"], choix["lng"]
        restants = [r for r in restants if r["nom"] != choix["nom"]]
    return route

# ─────────────────────────────────────────────
#  LOGO SVG
# ─────────────────────────────────────────────
LOGO_SVG = """<svg width="{w}" height="{w}" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="15" width="36" height="25" rx="4" fill="#F5F0E8" stroke="#0D0D0D" stroke-width="1.6"/>
  <path d="M4 22h36" stroke="#0D0D0D" stroke-width="1.2" stroke-linecap="square"/>
  <path d="M4 15c0-3 2.5-5.5 5.5-5.5h21c3 0 5.5 2.5 5.5 5.5" stroke="#0D0D0D" stroke-width="1.6" fill="none"/>
  <rect x="29" y="26" width="13" height="8" rx="4" fill="#0D0D0D"/>
  <circle cx="35.5" cy="30" r="1.8" fill="#F5F0E8"/>
  <g transform="translate(32,7) rotate(-35 4 3)">
    <path d="M0 3 L9 0 L9 6 Z" fill="#0D0D0D"/>
    <path d="M2 1.5 L-2 4 L0 3 Z" fill="#6B6560"/>
    <path d="M7 1 L5 5 L6.5 3 Z" fill="#6B6560"/>
  </g>
</svg>"""

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    lang_key = st.selectbox("", list(LANGS.keys()), label_visibility="collapsed")
    T = LANGS[lang_key]

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin:1rem 0 0.2rem">
      {LOGO_SVG.format(w=28)}
      <span style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;font-weight:400;color:#0D0D0D;letter-spacing:0.04em">Pouch Voyage</span>
    </div>
    <hr style="margin:0.6rem 0 1.2rem">
    """, unsafe_allow_html=True)

    ville_options = [f"{v['flag']} {v['nom']} ({v['iata']})" for v in VILLES_DEPART]
    ville_idx = st.selectbox(T["depart"], range(len(ville_options)), format_func=lambda i: ville_options[i])
    depart_ville = VILLES_DEPART[ville_idx]
    depart_iata  = depart_ville["iata"]

    st.caption(T["dates"])
    col1, col2 = st.columns(2)
    with col1:
        d1 = st.date_input("↗", value=date.today()+timedelta(days=30), min_value=date.today(), label_visibility="collapsed")
    with col2:
        d2 = st.date_input("↙", value=date.today()+timedelta(days=60), min_value=date.today(), label_visibility="collapsed")
    st.caption(f"{d1.strftime('%d/%m/%Y')} → {d2.strftime('%d/%m/%Y')}")

    st.caption(T["budget"])
    budget = st.slider("budget", min_value=500, max_value=15000, value=5000, step=100, label_visibility="collapsed")
    st.caption(T["budget_sel"].format(b=budget))

    st.caption(T["voyageurs"])
    c1, c2, c3 = st.columns(3)
    with c1: adultes = st.number_input(T["adultes"], min_value=1, max_value=9, value=1, step=1)
    with c2: enfants = st.number_input(T["enfants"], min_value=0, max_value=9, value=0, step=1)
    with c3: bebes   = st.number_input(T["bebes"],   min_value=0, max_value=9, value=0, step=1)

    st.caption(T["nb_dest"])
    nb_stops = st.slider("nb_stops", min_value=2, max_value=8, value=4, label_visibility="collapsed")

    fav = st.text_input(T["fav"], placeholder=T["fav_ph"])
    chercher = st.button(T["search"], use_container_width=True, type="primary")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption(T["powered"])

# ─────────────────────────────────────────────
#  CONTENU PRINCIPAL
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="logo-wrap">
  {LOGO_SVG.format(w=54)}
  <div class="main-title">Pouch Voyage</div>
</div>
<div class="subtitle">{T["subtitle"]}</div>
""", unsafe_allow_html=True)

if not chercher:
    st.info(T["fill_form"])
    st.stop()

nuits_total = (d2 - d1).days
if nuits_total <= 0:
    st.error(T["date_err"])
    st.stop()

d1_str    = d1.strftime("%Y-%m-%d")
d2_str    = d2.strftime("%Y-%m-%d")
fav_lower = fav.lower().strip()
nuits_par_etape = max(1, nuits_total // (nb_stops + 1))

# ── ONGLETS ───────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([T["tab_dest"], T["tab_back"], T["tab_meteo"], T["tab_cout"]])

# ═══════════════════════════════════════════════
#  ONGLET 1 — DESTINATIONS (grille 3 col + photos Unsplash)
# ═══════════════════════════════════════════════
with tab1:
    resultats = []
    for dest in DESTINATIONS:
        prix_est = prix_total(dest["prix_base"], adultes, enfants, bebes)
        if prix_est > budget: continue
        score = 2 if prix_est <= budget * 0.75 else 0
        nom_lower = dest["nom"].lower() + " " + dest["pays"].lower()
        if fav_lower and (fav_lower in nom_lower or any(m in fav_lower for m in nom_lower.split())):
            score += 10
        resultats.append({
            **dest, "prix_estime":prix_est, "nuits":nuits_total,
            "reste":budget-prix_est, "score":score, "is_favorite":score>=10,
            "url_sky": build_skyscanner_url(depart_iata, dest["iata"], d1_str, d2_str, adultes, enfants, bebes),
            "url_book":build_booking_url(dest["booking_id"], d1_str, d2_str, adultes, enfants),
        })
    resultats.sort(key=lambda x: (-x["score"], x["prix_estime"]))
    resultats = resultats[:12]

    total_v = adultes + enfants + bebes
    st.markdown(f'<div class="summary-box">{T["found"].format(n=len(resultats),nuits=nuits_total,v=total_v,b=budget)}</div>', unsafe_allow_html=True)

    if not resultats:
        st.markdown(f'<div class="no-result">{T["no_result"]}</div>', unsafe_allow_html=True)
    else:
        # Construire la grille HTML 3 colonnes avec cartes enrichies
        cards_html = '<div class="dest-grid">'
        for r in resultats:
            photo_url = UNSPLASH_PHOTOS.get(r["nom"], f"https://images.unsplash.com/photo-1488085061387-422e29b40080?w=600&q=80")

            # Ruban favori
            ribbon_html = ""
            if r["is_favorite"]:
                ribbon_html = f'<div class="fav-ribbon">{T["fav_label"]}</div>'

            # Prix (live ou estimé)
            live_vol   = get_skyscanner_prices(depart_iata, r["iata"], d1_str, d2_str, adultes)
            live_hotel = get_booking_hotel_price(r["booking_id"], d1_str, d2_str, adultes, nuits_total)

            if live_vol:
                price_label = T["price_live"]
                price_val   = f"{live_vol['price']:,} €"
            else:
                price_label = T["price_est"]
                price_val   = f"{r['prix_estime']:,} €"

            hotel_line = ""
            if live_hotel:
                hotel_line = f'<div class="dest-hotel">{T["hotel_live"].format(p=live_hotel["price_per_night"])}</div>'

            tags_str = "  ·  ".join(r["tags"])
            reste_str = T["reste"].format(r=r["reste"], n=r["nuits"])

            cards_html += f"""
<div class="dest-card">
  <div class="dest-photo-wrap">
    <img class="dest-photo" src="{photo_url}" alt="{r['nom']}" loading="lazy"/>
    {ribbon_html}
  </div>
  <div class="dest-body">
    <div class="dest-name">{r['flag']} {r['nom']}</div>
    <div class="dest-pays">{r['pays']}</div>
    <div class="dest-tags">{tags_str}</div>
    <div class="dest-price-label">{price_label}</div>
    <div class="dest-price">{price_val}</div>
    {hotel_line}
    <div class="dest-reste">{reste_str}</div>
    <div class="dest-btns">
      <a class="btn-vol" href="{r['url_sky']}" target="_blank" rel="noopener">{T['btn_sky']}</a>
      <a class="btn-hotel" href="{r['url_book']}" target="_blank" rel="noopener">{T['btn_book']}</a>
    </div>
  </div>
</div>"""

        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  ONGLET 2 — BACKPACKER
# ═══════════════════════════════════════════════
with tab2:
    route = build_backpacker_route(depart_ville, nb_stops, budget, adultes, enfants, bebes, nuits_par_etape)

    if not route:
        st.markdown(f'<div class="no-result">{T["back_no"]}</div>', unsafe_allow_html=True)
    else:
        nuits_total_back = nuits_par_etape * nb_stops
        st.markdown(f'<div class="itin-header">{T["back_title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="itin-subtitle">{T["back_sub"].format(n=nb_stops, nuits=nuits_total_back)}</div>', unsafe_allow_html=True)

        map_col, itin_col = st.columns([1.2, 1])

        with map_col:
            try:
                import json
                route_coords = [[depart_ville["lat"], depart_ville["lng"]]]
                for r in route:
                    route_coords.append([r["lat"], r["lng"]])
                route_coords.append([depart_ville["lat"], depart_ville["lng"]])

                markers_js = f"""
                  L.circleMarker([{depart_ville["lat"]},{depart_ville["lng"]}], {{
                    radius:8, color:'#0D0D0D', fillColor:'#F5F0E8', fillOpacity:1, weight:2
                  }}).addTo(map).bindPopup('<b>{depart_ville["flag"]} {depart_ville["nom"]}</b><br>Départ / Retour');
                """
                for idx, r in enumerate(route):
                    markers_js += f"""
                  L.circleMarker([{r["lat"]},{r["lng"]}], {{
                    radius:7, color:'#0D0D0D', fillColor:'#0D0D0D', fillOpacity:1, weight:2
                  }}).addTo(map).bindPopup('<b>{r["flag"]} {r["nom"]}</b><br>{r["pays"]}<br>~{r["prix_estime"]:,} €');
                    """

                coords_json = json.dumps(route_coords)
                map_html = f"""
<!DOCTYPE html><html><head>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body{{margin:0;background:#F5F0E8;}}
  #map{{height:420px;width:100%;background:#F5F0E8;}}
  .leaflet-tile{{filter:grayscale(1) contrast(0.9) brightness(1.05);}}
  .leaflet-container{{background:#EDE8DE;font-family:'Inter',sans-serif;}}
  .leaflet-popup-content-wrapper{{border-radius:0;border:1px solid #D4CFC6;box-shadow:none;}}
</style>
</head><body>
<div id="map"></div>
<script>
  var map = L.map('map', {{zoomControl:true, attributionControl:false}});
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png',{{maxZoom:18}}).addTo(map);
  var coords = {coords_json};
  L.polyline(coords, {{color:'#0D0D0D', weight:1.5, dashArray:'6,6', opacity:0.7}}).addTo(map);
  {markers_js}
  var bounds = L.latLngBounds(coords);
  map.fitBounds(bounds, {{padding:[30,30]}});
</script>
</body></html>"""
                st.components.v1.html(map_html, height=430)
            except Exception as e:
                st.caption(f"Carte non disponible : {e}")

        with itin_col:
            cout_vol_total = sum(r["prix_estime"] for r in route)
            cout_hotel_total = sum(r["prix_base"] * 0.05 * nuits_par_etape for r in route)
            cout_total = round(cout_vol_total * 0.4 + cout_hotel_total)
            pct = min(100, round(cout_total / budget * 100))
            reste_budget = budget - cout_total
            st.markdown(f"""
<div class="budget-bar-wrap">
  <div class="budget-bar-label">{T["back_budget_used"]} · {pct}%</div>
  <div class="budget-bar-bg"><div class="budget-bar-fill" style="width:{pct}%"></div></div>
  <div class="budget-numbers">
    <span>~{cout_total:,} €</span>
    <span>{T["back_budget_rest"]} ~{max(0,reste_budget):,} €</span>
  </div>
</div>
""", unsafe_allow_html=True)

            etapes = [{"nom":depart_ville["nom"],"flag":depart_ville["flag"],"pays":depart_ville["pays"],
                       "is_home":True,"tags":[]}] + \
                     [{"nom":r["nom"],"flag":r["flag"],"pays":r["pays"],"is_home":False,
                       "tags":r["tags"],"prix_estime":r["prix_estime"],
                       "iata":r["iata"],"booking_id":r["booking_id"]} for r in route] + \
                     [{"nom":depart_ville["nom"],"flag":depart_ville["flag"],"pays":depart_ville["pays"],
                       "is_home":True,"tags":[]}]

            cur_date = d1
            itin_html = ""
            for idx, etape in enumerate(etapes):
                is_last = idx == len(etapes) - 1
                dot = '<div class="itin-dot-home"></div>' if etape["is_home"] else '<div class="itin-dot"></div>'
                vline = "" if is_last else '<div class="itin-vline"></div>'

                if etape["is_home"]:
                    label = T["back_retour"] if is_last else T["back_depart"]
                    meta  = cur_date.strftime("%d %b %Y")
                    prix_line = ""
                    tags_line = ""
                else:
                    label = f"{etape['flag']} {etape['nom']}"
                    meta  = f"{cur_date.strftime('%d %b')} — {(cur_date+timedelta(days=nuits_par_etape)).strftime('%d %b %Y')} · {T['back_nuits'].format(n=nuits_par_etape)}"
                    prix_line = f'<div class="itin-price">~{etape["prix_estime"]:,} €</div>'
                    tags_line = f'<div class="itin-tags">{" · ".join(etape["tags"])}</div>'
                    cur_date += timedelta(days=nuits_par_etape)

                itin_html += f"""
<div class="itin-step">
  <div class="itin-line">{dot}{vline}</div>
  <div class="itin-content">
    <div class="itin-city">{label}</div>
    <div class="itin-meta">{meta}</div>
    {prix_line}{tags_line}
  </div>
</div>"""

            st.markdown(itin_html, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("Réservez chaque étape :")
        btn_cols = st.columns(min(len(route), 4))
        cur_date = d1
        for i, r in enumerate(route):
            d1_etape = cur_date.strftime("%Y-%m-%d")
            d2_etape = (cur_date + timedelta(days=nuits_par_etape)).strftime("%Y-%m-%d")
            prev_iata = depart_iata if i == 0 else route[i-1]["iata"]
            with btn_cols[i % len(btn_cols)]:
                st.markdown(f"**{r['flag']} {r['nom']}**")
                st.link_button(T["back_btn_sky"],
                               build_skyscanner_url(prev_iata, r["iata"], d1_etape, d2_etape, adultes, enfants, bebes),
                               use_container_width=True)
                st.link_button(T["back_btn_book"],
                               build_booking_url(r["booking_id"], d1_etape, d2_etape, adultes, enfants),
                               use_container_width=True)
            cur_date += timedelta(days=nuits_par_etape)

# ═══════════════════════════════════════════════
#  ONGLET 3 — MÉTÉO
# ═══════════════════════════════════════════════
with tab3:
    city_wx = st.text_input("🌍", placeholder=T["city_ph"], label_visibility="collapsed", key="city_wx")
    if city_wx:
        with st.spinner("..."):
            wx = get_weather(city_wx)
        if not wx:
            st.info(T["meteo_notfound"])
        else:
            st.markdown(f"### {wx['emoji']} {T['meteo_title'].format(city=wx['city'])}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🌡 Température", f"{wx['temp']}°C", T["meteo_feels"].format(f=wx['feels']))
            c2.metric("💧 Humidité", f"{wx['humidity']}%")
            c3.metric("💨 Vent", f"{wx['wind']} km/h")
            c4.metric("📊 Min / Max", f"{wx['temp_min']}° / {wx['temp_max']}°")
            st.caption(f"{wx['desc']}  ·  🌅 {wx['sunrise']}  🌇 {wx['sunset']}")
    else:
        st.info(T["fill_form"].replace("formulaire", "nom d'une ville"))

# ═══════════════════════════════════════════════
#  ONGLET 4 — COÛT DE LA VIE
# ═══════════════════════════════════════════════
with tab4:
    city_cout = st.text_input("🌍", placeholder=T["city_ph"], label_visibility="collapsed", key="city_cout")
    nuits_cout = st.slider("Nuits", min_value=1, max_value=90, value=7, label_visibility="collapsed")

    if city_cout:
        cout = get_cost_of_living(city_cout)
        if not cout:
            st.info(T["cout_notfound"])
        else:
            total_jour = cout["repas"] + cout["transport"] + cout["logement"] + cout["loisirs"]
            total_sejour = total_jour * nuits_cout

            st.markdown(f"### {T['cout_title'].format(city=city_cout.title())}")
            st.caption(T["cout_sub"])

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric(T["cout_repas"],     f"{cout['repas']} €",    T["cout_jour"])
            c2.metric(T["cout_transport"], f"{cout['transport']} €", T["cout_jour"])
            c3.metric(T["cout_logement"],  f"{cout['logement']} €",  T["cout_jour"])
            c4.metric(T["cout_loisirs"],   f"{cout['loisirs']} €",   T["cout_jour"])
            c5.metric(T["cout_total"],     f"{total_jour} €",        T["cout_jour"])

            st.markdown("<hr>", unsafe_allow_html=True)
            st.metric(f"💼 Budget estimé — {nuits_cout} nuits", f"{total_sejour:,} €",
                      delta=f"{'dans' if total_sejour <= budget else 'hors'} budget ({budget:,} €)",
                      delta_color="normal" if total_sejour <= budget else "inverse")

            pct = min(100, round(total_sejour / budget * 100))
            st.markdown(f"""
<div style="background:var(--cream2);border:1px solid var(--border);padding:1rem 1.2rem;margin-top:0.5rem">
  <div style="font-size:0.78rem;color:var(--muted);margin-bottom:6px">{pct}% du budget utilisé pour le séjour</div>
  <div style="background:var(--border);height:4px">
    <div style="background:var(--ink);height:4px;width:{pct}%"></div>
  </div>
</div>""", unsafe_allow_html=True)
    else:
        st.info(T["fill_form"].replace("formulaire", "nom d'une ville"))
