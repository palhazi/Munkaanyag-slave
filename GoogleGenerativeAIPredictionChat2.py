import os
import yfinance as yf
import google.generativeai as genai

# API kulcs beállítása (direkt vagy környezeti változó segítségével)
genai.configure(api_key='AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04')

# Példa: egy ticker elemzése (pl. GOOGL)
ticker_symbol = input("Add meg a részvény tickerét (pl. GOOGL): ").upper()
ticker = yf.Ticker(ticker_symbol)
data = ticker.history(period="1mo")
dates = data.index.strftime("%Y-%m-%d").tolist()
prices = data["Close"].round(2).tolist()
price_data_str = "\n".join(f"{d}: {p}" for d, p in zip(dates, prices))

# Első elemzés előállítása promptként
prompt = f"""Az alábbiakban bemutatom a(z) {ticker_symbol} részvény árfolyamadatait az elmúlt 1 hónapra:
{price_data_str}

Elemezd az adatokat röviden, és jósold meg a következő nap záró árfolyamát, indokold meg röviden a fő okokat!
"""

# Modell inicializálása (például gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# Indítsunk egy chat sessiont
chat = model.start_chat()

# Küldjük el az első üzenetet a chat sessionbe
response = chat.send_message(prompt)
print("\nElemzés és előrejelzés:")
print(response.text)  # Az első válasz kiírása

# Interaktív chat – további kérdések a tickerrel kapcsolatban
print(f"\nMost további kérdéseket tehetsz fel a(z) {ticker_symbol} részvény kapcsán ('exit' a kilépéshez).")

while True:
    user_input = input("\nTe: ")
    if user_input.lower() == "exit":
        print("Kilépés...")
        break

    try:
        # Küldjük a következő üzenetet a chat sessionbe
        response = chat.send_message(user_input)
        print("Bot:", response.text)
    except Exception as e:
        print("Hiba történt az API hívása során:", e)
