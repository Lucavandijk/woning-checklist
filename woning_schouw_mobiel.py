import streamlit as st
from datetime import date
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

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

# --- Google Sheets verbinding ---
@st.cache_resource
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
    sheet = client.open_by_key("1ZTGaSt8o51LGcW3lS3KJMeTVmSZZTt2PkzzFUbRrH-U").sheet1
    return sheet

# --- Google Drive verbinding ---
@st.cache_resource
def connect_to_drive():
    creds_dict = st.secrets["gcp_service_account"]
    scopes = ["https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)
    return service

# --- Upload bestand naar Google Drive met logging ---
def upload_file_to_drive(service, file, folder_id):
    st.write(f"Uploaden gestart: {file.name} (type: {file.type})")
    try:
        file_metadata = {
            'name': file.name,
            'parents': [folder_id]
        }
        media = MediaIoBaseUpload(io.BytesIO(file.getbuffer()), mimetype=file.type)
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        file_id = uploaded_file.get('id')
        # Maak direct een shareable link (publiek lezen)
        service.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"},
        ).execute()
        st.write(f"Bestand geüpload: {file.name} (ID: {file_id})")
        return f"https://drive.google.com/uc?id={file_id}"
    except Exception as e:
        st.error(f"Fout bij uploaden bestand: {e}")
        return None

# --- Verzamel foto-URL's ---
def get_photo_urls(fotos, drive_service, folder_id):
    urls = []
    if fotos:
        for foto in fotos:
            if foto is not None:
                url = upload_file_to_drive(drive_service, foto, folder_id)
                if url:
                    urls.append(url)
    return ", ".join(urls)

# --- Submit ---
if st.button("Verzenden"):
    # Basis check
    if not adres or not inspecteur or m2_woonoppervlak < 1:
        st.error("Vul alsjeblieft de verplichte velden in (adres, inspecteur, woonoppervlak).")
    else:
        try:
            sheet = connect_to_gsheet()
            drive_service = connect_to_drive()
            folder_id = "1JhQp5LPBq3F1XCe3wQX7WjoEnb3YEsnh"  # Pas aan naar jouw folder ID

            # Upload foto's en krijg URL's
            buitenmuren_foto_url = get_photo_urls([buitenmuren_foto], drive_service, folder_id)
            dakbedekking_foto_url = get_photo_urls([dakbedekking_foto], drive_service, folder_id)
            kozijnen_foto_url = get_photo_urls([kozijnen_foto], drive_service, folder_id)
            verwarming_foto_url = get_photo_urls([verwarming_foto], drive_service, folder_id)
            meterkast_foto_url = get_photo_urls([meterkast_foto], drive_service, folder_id)
            tuin_foto_urls = get_photo_urls(tuin_fotos, drive_service, folder_id) if tuin_checked else ""
            garage_foto_url = get_photo_urls([garage_foto], drive_service, folder_id)
            schuur_foto_url = get_photo_urls([schuur_foto], drive_service, folder_id)
            gebreken_foto_urls = get_photo_urls(gebreken_fotos, drive_service, folder_id)

            # Maak data rij - volgorde moet overeenkomen met kolommen in sheet!
            data = [
                adres,
                datum.strftime("%Y-%m-%d"),
                inspecteur,
                m2_woonoppervlak,
                energielabel,
                # Bouwkundige elementen
                "Ja" if buitenmuren_checked else "Nee",
                buitenmuren_foto_url,
                buitenmuren_opm,
                "Ja" if dakbedekking_checked else "Nee",
                dakbedekking_foto_url,
                dakbedekking_opm,
                "Ja" if kozijnen_checked else "Nee",
                kozijnen_foto_url,
                kozijnen_opm,
                ", ".join(geselecteerde_glas_types),
                "; ".join(f"{k}: {v}%" for k, v in glas_percentages.items()),
                vloer_type,
                vloer_opm,
                # Technische installaties
                "Ja" if verwarming_checked else "Nee",
                verwarming_type if verwarming_checked else "",
                verwarming_foto_url,
                verwarming_opm,
                "Ja" if elektra_checked else "Nee",
                elektra_opm,
                meterkast_type,
                meterkast_foto_url,
                "Ja" if ventilatie_checked else "Nee",
                ventilatie_opm,
                "Ja" if isolatie_checked else "Nee",
                ", ".join(isolatie_types),
                isolatie_opm,
                # Buitenruimte
                "Ja" if tuin_checked else "Nee",
                tuin_foto_urls,
                "Ja" if garage_checked else "Nee",
                garage_foto_url,
                garage_opm,
                "Ja" if schuur_checked else "Nee",
                schuur_foto_url,
                schuur_opm,
                "Ja" if toegankelijkheid_checked else "Nee",
                toegankelijkheid_opm,
                # Gebreken
                gebreken_tekst,
                gebreken_foto_urls,
                # Overig / juridisch
                "Ja" if erfdienstbaarheden_checked else "Nee",
                erfdienstbaarheden_opm,
                "Ja" if aanbouw_checked else "Nee",
                aanbouw_opm,
                algemene_indruk,
                opmerkingen_inspecteur,
            ]

            # Zorg dat data precies 46 kolommen heeft
            expected_columns = 46
            if len(data) < expected_columns:
                data += [''] * (expected_columns - len(data))
            elif len(data) > expected_columns:
                data = data[:expected_columns]

            # Debug info
            st.write(f"Aantal kolommen in data: {len(data)}")
            st.write(f"Data rij preview: {data}")

            # Voeg data in rij 2 toe (net onder de header)
            sheet.insert_row(data, 2, value_input_option='USER_ENTERED')

            st.success("Formulier succesvol opgeslagen in Google Sheets!")

        except Exception as e:
            st.error(f"Er is een fout opgetreden bij het opslaan: {e}")

