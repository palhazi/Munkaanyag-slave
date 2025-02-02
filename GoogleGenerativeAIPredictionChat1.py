import os
import yfinance as yf
import google.generativeai as genai

# API kulcs beállítása
genai.configure(api_key='AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04')

# Ticker bekérése a felhasználótól
ticker_symbol = input("Add meg a részvény tickerét (pl. GOOGL): ").upper()

# Lekérjük a részvény árfolyamadatait az elmúlt 1 hónapra
try:
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1mo")

    if data.empty:
        print(f"Nincs elérhető adat a(z) {ticker_symbol} tickerhez.")
        exit()

    # Kinyerjük a dátumokat és záró árakat
    dates = data.index.strftime("%Y-%m-%d").tolist()
    prices = data["Close"].round(2).tolist()

    # Összeállítjuk az adatokat egy szöveges blokkba
    price_data_str = "\n".join(f"{d}: {p}" for d, p in zip(dates, prices))

    # Prompt az elemzéshez és előrejelzéshez
    prompt = f"""Az alábbiakban bemutatom a(z) {ticker_symbol} részvény árfolyamadatait az elmúlt 1 hónapra:
{price_data_str}

Elemezd az adatokat röviden, és jósold meg a következő nap záró árfolyamát. Indokold meg röviden a jóslásod főbb okait!
"""

    # Modell inicializálása (pl. gemini-1.5-flash)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Kérés küldése a modellnek az elemzéshez
    response = model.generate_content(prompt)

    print("\nElemzés és előrejelzés:")
    print(response.text)

except Exception as e:
    print(f"Hiba történt az adatok lekérése vagy feldolgozása során: {e}")
    exit()

# Interaktív chat funkció
print("\nMost további kérdéseket tehetsz fel a(z) {ticker_symbol} részvényre vonatkozóan ('exit' a kilépéshez).")

conversation = [{"role": "system", "content": f"A(z) {ticker_symbol} részvény elemző asszisztensed vagyok."}]

while True:
    user_input = input("\nTe: ")
    
    if user_input.lower() == "exit":
        print("Kilépés...")
        break

    # Hozzáadjuk a felhasználói kérdést a beszélgetéshez
    conversation.append({"role": "user", "content": user_input})

    try:
        # Küldjük el a kérdést az AI-nak
        chat_response = model.generate_content(user_input)
        
        # A válasz kiírása és hozzáadása a beszélgetési kontextushoz
        print("Bot:", chat_response.text)
        conversation.append({"role": "assistant", "content": chat_response.text})
        
    except Exception as e:
        print(f"Hiba történt az API hívása során: {e}")
