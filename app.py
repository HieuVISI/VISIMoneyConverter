import streamlit as st
import requests

def fetch_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Lấy tỉ giá realtime từ API Frankfurter.
    Ví dụ: https://api.frankfurter.app/latest?from=USD&to=VND
    """
    url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        st.error("❌ Không kết nối được API")
        return None
    data = resp.json()
    if "rates" in data and to_currency in data["rates"]:
        return data["rates"][to_currency]
    else:
        st.error("❌ Không lấy được tỉ giá")
        return None


# ------------------ Giao diện ------------------
st.set_page_config(page_title="Currency Converter", page_icon="💱")
st.title("💱 Currency Converter → VND (Realtime)")

amount = st.number_input("Nhập số tiền:", min_value=0.0, step=1.0)
from_currency = st.selectbox("Chọn loại tiền gốc:", ["USD", "EUR", "CNY"])
to_currency = "VND"

if st.button("Chuyển đổi"):
    rate = fetch_exchange_rate(from_currency, to_currency)
    if rate:
        result = amount * rate
        st.success(
            f"💰 {amount} {from_currency} = {result:,.2f} {to_currency}\n\n"
            f"📊 Tỉ giá hiện tại: 1 {from_currency} = {rate:,.2f} {to_currency}"
        )
