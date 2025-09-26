import streamlit as st
import requests

# Bảng fallback nếu API không kết nối được
FALLBACK_RATES = {
    "USD": {"VND": 26399},
    "EUR": {"VND": 30828},
    "CNY": {"VND": 3700},
    "VND": {"USD": 1/26399, "EUR": 1/30828, "CNY": 1/3700},
}

def fetch_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Lấy tỉ giá realtime từ API Frankfurter.
    Nếu lỗi thì trả về fallback.
    """
    url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if "rates" in data and to_currency in data["rates"]:
                return data["rates"][to_currency]
    except Exception:
        pass  # Nếu lỗi, dùng fallback
    
    # fallback nếu API fail
    if from_currency in FALLBACK_RATES and to_currency in FALLBACK_RATES[from_currency]:
        return FALLBACK_RATES[from_currency][to_currency]
    else:
        st.error("❌ Không tìm thấy tỉ giá trong fallback")
        return None


# ------------------ Giao diện ------------------
st.set_page_config(page_title="Currency Converter", page_icon="💱")
st.title("💱 Currency Converter (Realtime / Fallback)")

amount = st.number_input("Nhập số tiền:", min_value=0.0, step=1.0)

# Danh sách tiền hỗ trợ
currencies = ["USD", "EUR", "CNY", "VND"]

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("Chọn loại tiền gốc:", currencies, index=0)
with col2:
    to_currency = st.selectbox("Chọn loại tiền muốn chuyển:", currencies, index=3)

if st.button("Chuyển đổi"):
    if from_currency == to_currency:
        st.info("Hai loại tiền giống nhau, kết quả = số tiền gốc")
    else:
        rate = fetch_exchange_rate(from_currency, to_currency)
        if rate:
            result = amount * rate
            st.success(
                f"💰 {amount} {from_currency} = {result:,.2f} {to_currency}\n\n"
                f"📊 Tỉ giá: 1 {from_currency} = {rate:,.2f} {to_currency}"
            )
