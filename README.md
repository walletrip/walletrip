# 🌍 Pouch Voyage

Application de recherche de voyages avec liens affiliés Travelpayout.

## 🚀 Déploiement sur Streamlit Cloud

### 1. Préparer le repo GitHub

Structure minimale requise :
```
ton-repo/
├── app.py
├── requirements.txt
└── README.md
```

### 2. Déployer sur Streamlit Cloud

1. Va sur [share.streamlit.io](https://share.streamlit.io)
2. Clique **New app**
3. Sélectionne ton repo GitHub + branche `main`
4. **Main file path** : `app.py`
5. Clique **Deploy!**

### 3. Ajouter les clés API (optionnel)

Les prix live (Skyscanner + Booking via RapidAPI) nécessitent des clés.  
Sans clés, l'app fonctionne avec les **prix estimés statiques**.

Dans Streamlit Cloud → ton app → **Settings → Secrets** :

```toml
SKYSCANNER_API_KEY = "ta_cle_rapidapi_skyscanner"
BOOKING_API_KEY    = "ta_cle_rapidapi_booking"
```

### 4. Test local

```bash
pip install streamlit requests
streamlit run app.py
```

Puis ouvre [http://localhost:8501](http://localhost:8501)

---

## 🔑 Affiliation

- Réseau : **Travelpayout**
- ID affilié : `731169`
- Skyscanner via `tp.media` (p=4114)
- Booking.com via `tp.media` (p=4)
