import streamlit as st
from datetime import date

st.set_page_config(page_title="Woning Schouw Checklist", layout="centered")

# --- Custom CSS styling ---
st.markdown(
    """
    <style>
    /* Achtergrond en tekst */
    .main {
        background-color: #f9faff;
        color: #111111;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 1rem;
    }

    /* Headers */
    h1, h2, h3 {
        color: #0099FF !important;
        font-weight: 700;
    }

    /* Buttons - groter en meer padding voor mobiel */
    div.stButton > button {
        background-color: #0099FF;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.75em 1.5em;
        font-weight: 600;
        font-size: 1.1rem;
        transition: background-color 0.3s ease;
        min-width: 100%;
    }
    div.stButton > button:hover {
        background-color: #007acc;
        color: white;
    }

    /* Inputs en textareas groter */
    input, textarea, select {
        font-size: 1rem !important;
        padding: 0.5em !important;
    }

    /* Checkbox grotere klikarea */
    label[data-testid="stMarkdownContainer"] > div > div > input[type="checkbox"] {
        accent-color: #0099FF;
        width: 1.5em;
        height: 1.5em;
        cursor: pointer;
    }

    /* Links */
    a {
        color: #0099FF !important;
    }

    /* Expander header kleur */
    button[aria-expanded="false"], button[aria-expanded="true"] {
        color: #0099FF !important;
        font-weight: 600;
        font-size: 1rem;
    }

    /* Maak alles mobielvriendelijk */
    @media (max-width: 600px) {
        .css-1d391kg {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏠 Woning Schouw Checklist")

# --- Algemene informatie ---
st.header("Algemene informatie")
adres = st.text_input("Adres woning")
datum = st.date_input("Datum schouw", value=date.today())
inspecteur = st.text_input("Naam inspecteur")

# Verplichte velden woonoppervlak en energielabel
m2_woonoppervlak = st.number_input("Woonoppervlak (m²) *", min_value=1, step=1)
energielabel_opties = ["A++", "A+", "A", "B", "C", "D", "E", "F", "G", "Onbekend"]
energielabel = st.selectbox("Bekend energielabel *", energielabel_opties)

st.markdown("---")

# --- Bouwkundige elementen ---
st.header("Bouwkundige elementen")

buitenmuren_checked = st.checkbox("Buitenmuren / gevels gecontroleerd")
with st.expander("Details buitenmuren / gevels"):
    buitenmuren_foto = st.file_uploader("Foto buitenmuren / gevels", type=["jpg", "png", "jpeg"], key="buitenmuren_foto")
    buitenmuren_opm = st.text_area("Opmerkingen buitenmuren / gevels")

dakbedekking_checked = st.checkbox("Dakbedekking gecontroleerd")
with st.expander("Details dakbedekking"):
    dakbedekking_foto = st.file_uploader("Foto dakbedekking", type=["jpg", "png", "jpeg"], key="dakbedekking_foto")
    dakbedekking_opm = st.text_area("Opmerkingen dakbedekking")

kozijnen_checked = st.checkbox("Kozijnen/deuren/ramen gecontroleerd")
with st.expander("Details kozijnen/deuren/ramen"):
    kozijnen_foto = st.file_uploader("Foto kozijnen/deuren/ramen", type=["jpg", "png", "jpeg"], key="kozijnen_foto")
    kozijnen_opm = st.text_area("Opmerkingen kozijnen/deuren/ramen")

with st.expander("Type glas (meerdere mogelijk)"):
    glas_types = ["Enkel", "Dubbel", "HR", "HR+", "HR++", "Vacuüm"]
    geselecteerde_glas_types = st.multiselect("Selecteer glas types (1-3)", glas_types, max_selections=3)

    glas_percentages = {}
    if geselecteerde_glas_types:
        st.write("Vul per geselecteerd glas type het percentage in (totaal maximaal 100%)")
        totaal_percentage = 0
        for glas in geselecteerde_glas_types:
            pct = st.number_input(f"Percentage {glas}", min_value=0, max_value=100, value=0, step=5, key=f"glas_pct_{glas}")
            glas_percentages[glas] = pct
            totaal_percentage += pct

        if totaal_percentage > 100:
            st.error(f"Het totaal van alle percentages is {totaal_percentage}%. Dit mag niet meer dan 100% zijn.")
    else:
        st.info("Selecteer minimaal één glas type.")

with st.expander("Type vloer"):
    vloer_type = st.selectbox("Type vloer", ["Hout", "Beton", "Anders (specificeer hieronder)"])
    vloer_opm = st.text_area("Opmerkingen type vloer")

st.markdown("---")

# --- Technische installaties ---
st.header("Technische installaties")

verwarming_checked = st.checkbox("Verwarming gecontroleerd")
with st.expander("Details verwarming"):
    verwarming_type = st.selectbox("Type verwarmingsinstallatie", ["Gas", "Stadsverwarming", "Hybride warmtepomp", "Full-electric warmtepomp"])
    verwarming_foto = st.file_uploader("Foto verwarmingsinstallatie", type=["jpg", "png", "jpeg"], key="verwarming_foto")
    verwarming_opm = st.text_area("Opmerkingen verwarming")

elektra_checked = st.checkbox("Elektra gecontroleerd")
with st.expander("Details elektra"):
    elektra_opm = st.text_area("Opmerkingen elektra")

with st.expander("Type meterkast"):
    meterkast_type = st.selectbox("Type meterkast", ["Oud", "1 fase", "3 fase"])
    meterkast_foto = st.file_uploader("Foto meterkast", type=["jpg", "png", "jpeg"], key="meterkast_foto")

ventilatie_checked = st.checkbox("Ventilatie gecontroleerd")
with st.expander("Details ventilatie"):
    ventilatie_opm = st.text_area("Opmerkingen ventilatie")

isolatie_checked = st.checkbox("Isolatie gecontroleerd")
with st.expander("Details isolatie"):
    isolatie_types = st.multiselect("Soorten isolatie aanwezig", ["Dak", "Muur", "Vloer", "Glas"])
    isolatie_opm = st.text_area("Opmerkingen isolatie")

st.markdown("---")

# --- Buitenruimte ---
st.header("Buitenruimte")

tuin_checked = st.checkbox("Tuin/balkon gecontroleerd")
with st.expander("Details tuin/balkon"):
    tuin_fotos = st.file_uploader("Foto('s) tuin/balkon", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="tuin_fotos")

garage_checked = st.checkbox("Garage/oprit gecontroleerd")
with st.expander("Details garage/oprit"):
    garage_foto = st.file_uploader("Foto garage/oprit", type=["jpg", "png", "jpeg"], key="garage_foto")
    garage_opm = st.text_area("Opmerkingen garage/oprit")

schuur_checked = st.checkbox("Schuur/berging gecontroleerd")
with st.expander("Details schuur/berging"):
    schuur_foto = st.file_uploader("Foto schuur/berging", type=["jpg", "png", "jpeg"], key="schuur_foto")
    schuur_opm = st.text_area("Opmerkingen schuur/berging")

toegankelijkheid_checked = st.checkbox("Toegankelijkheid woning gecontroleerd")
with st.expander("Details toegankelijkheid"):
    toegankelijkheid_opm = st.text_area("Opmerkingen toegankelijkheid")

st.markdown("---")

# --- Gebreken ---
st.header("Gebreken")

gebreken_tekst = st.text_area("Algemene opmerkingen over gebreken")
gebreken_fotos = st.file_uploader("Foto('s) van gebreken", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="gebreken_fotos")

st.markdown("---")

# --- Overig / juridisch ---
st.header("Overig / juridisch")

erfdienstbaarheden_checked = st.checkbox("Erfdienstbaarheden aanwezig")
with st.expander("Details erfdienstbaarheden"):
    erfdienstbaarheden_opm = st.text_area("Opmerkingen erfdienstbaarheden")

aanbouw_checked = st.checkbox("Aan- of bijgebouwen aanwezig")
with st.expander("Details aanbouw"):
    aanbouw_opm = st.text_area("Opmerkingen aanbouw")

algemene_indruk = st.text_area("Algemene indruk woning")
opmerkingen_inspecteur = st.text_area("Algemene opmerkingen inspecteur")

# --- Verzamel alle gegevens ---
if st.button("✔️ Sla checklist op als JSON"):

    if m2_woonoppervlak == 0:
        st.error("Vul het woonoppervlak in (m2)")
    elif energielabel == "Onbekend":
        st.error("Selecteer het energielabel")
    else:
        data = {
            "adres": adres,
            "datum": str(datum),
            "inspecteur": inspecteur,
            "woonoppervlak_m2": m2_woonoppervlak,
            "energielabel": energielabel,
            "bouwkundige_elementen": {
                "buitenmuren": {"gecontroleerd": buitenmuren_checked, "opmerkingen": buitenmuren_opm, "foto": (buitenmuren_foto.name if buitenmuren_foto else None)},
                "dakbedekking": {"gecontroleerd": dakbedekking_checked, "opmerkingen": dakbedekking_opm, "foto": (dakbedekking_foto.name if dakbedekking_foto else None)},
                "kozijnen": {"gecontroleerd": kozijnen_checked, "opmerkingen": kozijnen_opm, "foto": (kozijnen_foto.name if kozijnen_foto else None)},
                "type_glas": {glas: glas_percentages.get(glas, 0) for glas in geselecteerde_glas_types},
                "type_vloer": vloer_type,
                "vloer_opmerkingen": vloer_opm,
            },
            "technische_installaties": {
                "verwarming": {"gecontroleerd": verwarming_checked, "opmerkingen": verwarming_opm, "type": verwarming_type, "foto": (verwarming_foto.name if verwarming_foto else None)},
                "elektra": {"gecontroleerd": elektra_checked, "opmerkingen": elektra_opm},
                "meterkast": {"type": meterkast_type, "foto": (meterkast_foto.name if meterkast_foto else None)},
                "ventilatie": {"gecontroleerd": ventilatie_checked, "opmerkingen": ventilatie_opm},
                "isolatie": {"gecontroleerd": isolatie_checked, "soorten": isolatie_types, "opmerkingen": isolatie_opm},
            },
            "buitenruimte": {
                "tuin": {"gecontroleerd": tuin_checked, "foto's": [f.name for f in tuin_fotos] if tuin_fotos else []},
                "garage": {"gecontroleerd": garage_checked, "opmerkingen": garage_opm, "foto": (garage_foto.name if garage_foto else None)},
                "schuur": {"gecontroleerd": schuur_checked, "opmerkingen": schuur_opm, "foto": (schuur_foto.name if schuur_foto else None)},
                "toegankelijkheid": {"gecontroleerd": toegankelijkheid_checked, "opmerkingen": toegankelijkheid_opm},
            },
            "gebreken": {
                "tekst": gebreken_tekst,
                "foto's": [f.name for f in gebreken_fotos] if gebreken_fotos else [],
            },
            "overig": {
                "erfdienstbaarheden": {"aanwezig": erfdienstbaarheden_checked, "opmerkingen": erfdienstbaarheden_opm},
                "aanbouw": {"aanwezig": aanbouw_checked, "opmerkingen": aanbouw_opm},
                "algemene_indruk": algemene_indruk,
                "opmerkingen_inspecteur": opmerkingen_inspecteur,
            }
        }

        import json
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        st.code(json_data, language="json")

        # Opslaan als bestand lokaal
        with open("woning_schouw_data.json", "w", encoding="utf-8") as f:
            f.write(json_data)
        st.success("Checklist succesvol opgeslagen als woning_schouw_data.json")
