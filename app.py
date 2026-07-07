import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# =========================
# Load Model
# =========================
model = load_model("model/skin_model.h5")

# =========================
# Classes
# =========================
classes = [
    "Acne and Rosacea",
    "Actinic Keratosis Basal Cell Carcinoma",
    "Atopic Dermatitis",
    "Cellulitis Impetigo and other Bacterial Infections",
    "Eczema",
    "Exanthems and Drug Eruptions",
    "Herpes HPV and other STDs",
    "Light Diseases and Disorders of Pigmentation",
    "Lupus and other Connective Tissue Diseases",
    "Melanoma Skin Cancer Nevi and Moles",
    "Poison Ivy and Contact Dermatitis",
    "Psoriasis Lichen Planus and related",
    "Seborrheic Keratoses and other Benign Tumors",
    "Systemic Disease",
    "Tinea Ringworm Candidiasis and other Fungal",
    "Urticaria Hives",
    "Vascular Tumors",
    "Vasculitis",
    "Warts Molluscum and other Viral Infections"
]

# =========================
# Disease Information
# =========================
disease_info = {

    "Acne and Rosacea": {
        "desc_en": "Acne and rosacea are skin conditions causing pimples and facial redness.",
        "desc_hi": "एक्ने और रोजेशिया में पिंपल और चेहरे पर लालिमा होती है।",
        "treat_en": "Use gentle cleansers and avoid oily products.",
        "treat_hi": "हल्का फेस वॉश करें और तैलीय उत्पादों से बचें।",
        "desi": "नीम और हल्दी का उपयोग फायदेमंद हो सकता है।",
        "medicines": [
            {"name": "Benzoyl Peroxide gel"},
            {"name": "Adapalene"},
            {"name": "Doxycycline"}
        ]
    },

    "Eczema": {
        "desc_en": "Eczema causes dry, itchy, and irritated skin.",
        "desc_hi": "एक्जिमा में त्वचा सूखी और खुजलीदार हो जाती है।",
        "treat_en": "Use moisturizers and avoid harsh soaps.",
        "treat_hi": "मॉइस्चराइजर का उपयोग करें और कड़े साबुन से बचें।",
        "desi": "नारियल तेल त्वचा को शांत करता है।",
        "medicines": [
            {"name": "Topical steroids"},
            {"name": "Cetirizine"},
            {"name": "Moisturizers"}
        ]
    },

    "Tinea Ringworm Candidiasis and other Fungal": {
        "desc_en": "Fungal infections causing itching and rashes.",
        "desc_hi": "फंगल संक्रमण जिससे खुजली और चकत्ते होते हैं।",
        "treat_en": "Use antifungal creams and keep skin dry.",
        "treat_hi": "एंटीफंगल क्रीम लगाएं और त्वचा सूखी रखें।",
        "desi": "नीम और हल्दी उपयोगी हो सकते हैं।",
        "medicines": [
            {"name": "Clotrimazole"},
            {"name": "Terbinafine"},
            {"name": "Fluconazole"}
        ]
    },

    "Psoriasis Lichen Planus and related": {
        "desc_en": "Chronic condition causing scaly patches.",
        "desc_hi": "यह रोग त्वचा पर परतदार धब्बे बनाता है।",
        "treat_en": "Use medicated creams and consult doctor.",
        "treat_hi": "दवा का उपयोग करें और डॉक्टर से मिलें।",
        "desi": "एलोवेरा जेल राहत दे सकता है।",
        "medicines": [
            {"name": "Topical steroids"},
            {"name": "Methotrexate"},
            {"name": "Vitamin D analogs"}
        ]
    },

    "Urticaria Hives": {
        "desc_en": "Raised itchy welts caused by allergies.",
        "desc_hi": "एलर्जी से त्वचा पर सूजन और खुजली होती है।",
        "treat_en": "Avoid triggers and take antihistamines.",
        "treat_hi": "ट्रिगर से बचें और दवा लें।",
        "desi": "ठंडा पानी राहत देता है।",
        "medicines": [
            {"name": "Cetirizine"},
            {"name": "Loratadine"},
            {"name": "Fexofenadine"}
        ]
    },

    "Atopic Dermatitis": {
        "desc_en": "A chronic condition causing itchy and inflamed skin.",
        "desc_hi": "यह एक दीर्घकालिक त्वचा रोग है जिसमें खुजली और सूजन होती है।",
        "treat_en": "Keep skin moisturized and avoid triggers.",
        "treat_hi": "त्वचा को नम रखें और ट्रिगर से बचें।",
        "desi": "नारियल तेल लगाने से राहत मिल सकती है।",
        "medicines": [
            {"name": "Hydrocortisone"},
            {"name": "Tacrolimus"},
            {"name": "Moisturizers"}
        ]
    },

    "Warts Molluscum and other Viral Infections": {
        "desc_en": "Viral infections causing bumps on skin.",
        "desc_hi": "वायरल संक्रमण जिससे त्वचा पर छोटे उभार होते हैं।",
        "treat_en": "Avoid touching and consult doctor.",
        "treat_hi": "छूने से बचें और डॉक्टर से मिलें।",
        "desi": "लहसुन का उपयोग कुछ मामलों में मदद कर सकता है।",
        "medicines": [
            {"name": "Salicylic acid"},
            {"name": "Cryotherapy"},
            {"name": "Imiquimod"}
        ]
    }
}

# =========================
# Symptoms Dictionary
# =========================
symptom_data = {

    "Acne and Rosacea": [
        "pimples",
        "acne",
        "redness",
        "oily skin"
    ],

    "Eczema": [
        "itching",
        "dry skin",
        "rash",
        "skin rash",
        "skin rashes",
        "red patches"
    ],

    "Tinea Ringworm Candidiasis and other Fungal": [
        "fungal infection",
        "ringworm",
        "itching",
        "red circle"
    ],

    "Psoriasis Lichen Planus and related": [
        "scaly skin",
        "white patches",
        "itchy skin"
    ],

    "Urticaria Hives": [
        "allergy",
        "swelling",
        "hives",
        "itching"
    ],

    "Atopic Dermatitis": [
        "skin inflammation",
        "itchy skin",
        "dryness"
    ],

    "Warts Molluscum and other Viral Infections": [
        "warts",
        "viral bumps",
        "skin bumps"
    ]
}

# =========================
# App Title
# =========================
st.title("🩺 Skin Disease Detection System")

# =========================
# Image Upload Section
# =========================
file = st.file_uploader("📸 Upload Skin Image")

if file:

    img = Image.open(file)

    st.image(img, caption="Uploaded Image", use_container_width=True)

    img = np.array(img)

    img = cv2.resize(img, (128, 128))

    img = img / 255.0

    img = np.reshape(img, (1, 128, 128, 3))

    pred = model.predict(img)

    result = classes[np.argmax(pred)]

    st.success(f"Detected Disease: {result}")

    # Get info
    info = disease_info.get(result)

    if info:

        st.subheader("📖 Description")
        st.write(info["desc_en"])
        st.write(info["desc_hi"])

        st.subheader("💊 Treatment")
        st.write(info["treat_en"])
        st.write(info["treat_hi"])

        st.subheader("🌿 Home Remedy")
        st.write(info["desi"])

        st.subheader("💊 Recommended Medicines")

        for med in info.get("medicines", []):
            st.write("👉", med["name"])

    else:
        st.error("No detailed information available.")

# =========================
# Chatbot Section
# =========================
st.markdown("---")

st.title("🤖 Skin Disease Chatbot")

user_input = st.text_input(
    "Enter your symptoms (Example: itching, red rash, pimples)"
)

if user_input:

    user_input = user_input.lower()

    matched_disease = None

    for disease, symptoms in symptom_data.items():

        for symptom in symptoms:

            if symptom in user_input:
                matched_disease = disease
                break

        if matched_disease:
            break

    if matched_disease:

        info = disease_info[matched_disease]

        st.success(f"Possible Disease: {matched_disease}")

        st.subheader("📖 Description")
        st.write(info["desc_en"])
        st.write(info["desc_hi"])

        st.subheader("💊 Treatment")
        st.write(info["treat_en"])
        st.write(info["treat_hi"])

        st.subheader("🌿 Home Remedy")
        st.write(info["desi"])

        st.subheader("💊 Medicines")

        for med in info.get("medicines", []):
            st.write("👉", med["name"])

    else:
        st.error("No matching disease found. Please consult a doctor.")

# =========================
# Hospital Finder Section
# =========================

st.markdown("---")
st.title("🏥 Nearby Hospital Finder")

location = st.text_input(
    "Enter Your City or Location",
    placeholder="Example: Varanasi"
)

if location:

    geolocator = Nominatim(user_agent="skin_app")

    loc = geolocator.geocode(location)

    if loc:

        lat = loc.latitude
        lon = loc.longitude

        st.success(f"Location Found: {location}")

        # Create map
        m = folium.Map(location=[lat, lon], zoom_start=12)

        # User marker
        folium.Marker(
            [lat, lon],
            tooltip="Your Location",
            popup="You are here",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        # Dummy hospital locations
        hospitals = [
            ["City Hospital", lat + 0.01, lon + 0.01],
            ["Skin Care Clinic", lat - 0.01, lon - 0.01],
            ["Apollo Hospital", lat + 0.02, lon - 0.02],
        ]

        for hospital in hospitals:

            folium.Marker(
                [hospital[1], hospital[2]],
                tooltip=hospital[0],
                popup=hospital[0],
                icon=folium.Icon(color="red", icon="plus-sign")
            ).add_to(m)

        st_folium(m, width=700, height=500)

    else:
        st.error("Location not found")