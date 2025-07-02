import streamlit as st
from datetime import date

import gspread
from google.oauth2.service_account import Credentials

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


# --- Functies voor Google Sheets ---

def connect_to_gsheet():
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1ZTGaSt8o51LGcW3lS3KJMeTVmZmEK0hRBhNVpZb9gI8").sheet1
    return sheet

def flatten_data_for_sheet(data):
    # Maak een vlakke lijst met volgorde passend bij kolommen in je Google Sheet
    flat = [
        data.get("adres", ""),
        data.get("datum", ""),
        data.get("inspecteur", ""),
        data.get("m2_woonoppervlak", ""),
        data.get("energielabel", ""),
        data.get("buitenmuren_checked", ""),
        data.get("buitenmuren_opm", ""),
        data.get("dakbedekking_checked", ""),
        data.get("dakbedekking_opm", ""),
        data.get("kozijnen_checked", ""),
        data.get("kozijnen_opm", ""),
        ", ".join(data.get("geselecteerde_glas_types", [])),
        "; ".join(f"{k}: {v}%" for k, v in data.get("glas_percentages", {}).items()),
        data.get("vloer_type", ""),
        data.get("vloer_opm", ""),
        data.get("verwarming_checked", ""),
        data.get("verwarming_type", ""),
        data.get("verwarming_opm", ""),
        data.get("elektra_checked", ""),
        data.get("elektra_opm", ""),
        data.get("meterkast_type", ""),
        data.get("ventilatie_checked", ""),
        data.get("ventilatie_opm", ""),
        data.get("isolatie_checked", ""),
        ", ".join(data.get("isolatie_types", [])),
        data.get("isolatie_opm", ""),
        data.get("tuin_checked", ""),
        data.get("garage_checked", ""),
        data.get("garage_opm", ""),
        data.get("schuur_checked", ""),
        data.get("schuur_opm", ""),
        data.get("toegankelijkheid_checked", ""),
        data.get("toegankelijkheid_opm", ""),
        data.get("gebreken_tekst", ""),
        data.get("erfdienstbaarheden_checked", ""),
        data.get("erfdienstbaarheden_opm", ""),
        data.get("aanbouw_checked", ""),
        data.get("aanbouw_opm", ""),
        data.get("algemene_indruk", ""),
        data.get("opmerkingen_inspecteur", ""),
    ]
    return flat


# --- Button om op te slaan ---

if st.button("Opslaan checklist"):
    data = {
        "adres": adres,
        "datum": datum.strftime("%Y-%m-%d"),
        "inspecteur": inspecteur,
        "m2_woonoppervlak": m2_woonoppervlak,
        "energielabel": energielabel,
        "buitenmuren_checked": buitenmuren_checked,
        "buitenmuren_opm": buitenmuren_opm,
        "dakbedekking_checked": dakbedekking_checked,
        "dakbedekking_opm": dakbedekking_opm,
        "kozijnen_checked": kozijnen_checked,
        "kozijnen_opm": kozijnen_opm,
        "geselecteerde_glas_types": geselecteerde_glas_types,
        "glas_percentages": glas_percentages,
        "vloer_type": vloer_type,
        "vloer_opm": vloer_opm,
        "verwarming_checked": verwarming_checked,
        "verwarming_type": verwarming_type,
        "verwarming_opm": verwarming_opm,
        "elektra_checked": elektra_checked,
        "elektra_opm": elektra_opm,
        "meterkast_type": meterkast_type,
        "ventilatie_checked": ventilatie_checked,
        "ventilatie_opm": ventilatie_opm,
        "isolatie_checked": isolatie_checked,
        "isolatie_types": isolatie_types,
        "isolatie_opm": isolatie_opm,
        "tuin_checked": tuin_checked,
        "garage_checked": garage_checked,
        "garage_opm": garage_opm,
        "schuur_checked": schuur_checked,
        "schuur_opm": schuur_opm,
        "toegankelijkheid_checked": toegankelijkheid_checked,
        "toegankelijkheid_opm": toegankelijkheid_opm,
        "gebreken_tekst": gebreken_tekst,
        "erfdienstbaarheden_checked": erfdienstbaarheden_checked,
        "erfdienstbaarheden_opm": erfdienstbaarheden_opm,
        "aanbouw_checked": aanbouw_checked,
        "aanbouw_opm": aanbouw_opm,
        "algemene_indruk": algemene_indruk,
        "opmerkingen_inspecteur": opmerkingen_inspecteur,
    }

    # Opslaan lokaal
    import json
    filename = "woning_schouw_data.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    st.success(f"Checklist succesvol opgeslagen als {filename}")

    # Opslaan in Google Sheets
    try:
        sheet = connect_to_gsheet()
        flat_row = flatten_data_for_sheet(data)
        sheet.append_row(flat_row)
        st.success("✅ Gegevens ook succesvol opgeslagen in Google Sheets!")
    except Exception as e:
        st.error(f"Fout bij opslaan in Google Sheets: {e}")

        with open("woning_schouw_data.json", "w", encoding="utf-8") as f:
            f.write(json_data)
        st.success("Checklist succesvol opgeslagen als woning_schouw_data.json")
