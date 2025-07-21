import os
from dotenv import load_dotenv
import streamlit as st
import requests
import time

load_dotenv()

API_KEY = os.getenv("API_KEY")

CURRENCY_LIST_URL = f"https://api.freecurrencyapi.com/v1/currencies?apikey={API_KEY}"
EXCHANGE_RATE_URL = "https://api.freecurrencyapi.com/v1/latest"

# Load once & cache
@st.cache_data
def get_currency_list():
    try:
        res = requests.get(CURRENCY_LIST_URL)
        res.raise_for_status()
        data = res.json()["data"]
        return {code: details["name"] for code, details in data.items()}
    except Exception as e:
        st.error("❌ Error fetching currency list.")
        return {}

def convert_currency(from_currency, to_currency, amount):
    try:
        res = requests.get(f"{EXCHANGE_RATE_URL}?apikey={API_KEY}&base_currency={from_currency}")
        res.raise_for_status()
        rate = res.json()["data"][to_currency]
        return round(amount * rate, 2)
    except Exception as e:
        st.error("❌ Conversion failed. Please check the currencies and try again.")
        return None

# Set up page
st.set_page_config(page_title="💱 Currency Converter", page_icon="🌍", layout="centered")

# Title with animation effect
st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>💸 Currency Converter</h1>",
    unsafe_allow_html=True
)

# Add subtle animated progress bar
with st.spinner("Loading currencies..."):
    currency_dict = get_currency_list()
    time.sleep(0.5)

if not currency_dict:
    st.stop()

currency_codes = list(currency_dict.keys())

# Responsive layout
st.markdown("---")
st.markdown("### 🔄 Select Currencies")

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From", options=currency_codes, format_func=lambda x: f"{x} - {currency_dict[x]}")
with col2:
    to_currency = st.selectbox("To", options=currency_codes, format_func=lambda x: f"{x} - {currency_dict[x]}")

amount = st.number_input(f"💰 Enter amount in {from_currency}", min_value=0.0, step=1.0, format="%.2f")

# Convert button with loading animation
if st.button("🔁 Convert"):
    if from_currency == to_currency:
        st.warning("⚠️ Choose two different currencies.")
    else:
        with st.spinner("Converting..."):
            result = convert_currency(from_currency, to_currency, amount)
            time.sleep(0.3)
            if result is not None:
                st.success(f"✅ {amount} {from_currency} = {result} {to_currency}")

# Footer
st.markdown("---")

