import streamlit as st
import sqlite3
import pandas as pd

# Připojení k databázi
conn = sqlite3.connect("pujcovna.db")

# Načtení dat
stroje = pd.read_sql_query("SELECT * FROM stroje", conn)
firmy = pd.read_sql_query("SELECT * FROM firmy", conn)

st.set_page_config(page_title="Půjčovna stavebních strojů", layout="centered")

st.title("🏗️ Půjčovna stavebních strojů")

# Výběr firmy
st.subheader("Informace o klientovi")
firma = st.selectbox("Vyber firmu:", firmy["nazev"].tolist())

if firma:
    data_firmy = firmy[firmy["nazev"] == firma].iloc[0]
    st.write(f"**Adresa:** {data_firmy['adresa']}")
    st.write(f"**IČO:** {data_firmy['ico']}")
    st.write(f"**Kontaktní osoba:** {data_firmy['kontakt']}")
    st.write(f"**Sleva:** {data_firmy['sleva']*100:.0f}%")

# Výběr strojů
st.subheader("Výběr strojů")
vybrane_stroje = []
celkem = 0

for i in range(1, 6):
    stroj = st.selectbox(f"Stroj {i}:", ["-"] + stroje["nazev"].tolist(), key=f"stroj_{i}")
    dny = st.number_input(f"Počet dní pro stroj {i}:", min_value=0, max_value=30, value=0, key=f"dny_{i}")
    
    if stroj != "-" and dny > 0:
        info = stroje[stroje["nazev"] == stroj].iloc[0]
        cena = info["cena_za_den"] * dny
        celkem += cena
        vybrane_stroje.append(f"{stroj} ({dny} dní × {info['cena_za_den']} Kč/den = {cena} Kč)")

# Výpočet celkové ceny
if st.button("💰 Spočítat cenu"):
    if len(vybrane_stroje) == 0:
        st.warning("Nevybral jsi žádný stroj.")
    else:
        sleva = data_firmy["sleva"]
        po_sleve = celkem * (1 - sleva)

        st.markdown("---")
        st.subheader("🧾 Souhrn objednávky")
        for s in vybrane_stroje:
            st.write("-", s)

        st.write(f"**Sleva:** {sleva*100:.0f}%")
        st.write(f"**Celková cena:** {celkem:.2f} Kč")
        st.success(f"**Cena po slevě:** {po_sleve:.2f} Kč")

st.markdown("---")
st.caption("© 2025 Půjčovna FAST VUT — vytvořil student Filip Vaja🎓")

