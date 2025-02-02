import os
import yfinance as yf
import google.generativeai as genai

# API kulcs beállítása a kódban
genai.configure(api_key="AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04")

# Lekérjük a Google (GOOGL) részvény árfolyam adatait az elmúlt 1 hónapra
ticker = yf.Ticker("GOOGL")
data = ticker.history(period="1mo")
dates = data.index.strftime("%Y-%m-%d").tolist()
prices = data["Close"].round(2).tolist()

# Összeállítjuk az adatokat egy szöveges blokkba
price_data_str = "\n".join(f"{d}: {p}" for d, p in zip(dates, prices))

# Prompt összerakása, hogy elemezze az árfolyam adatokat és jóslatot adjon
prompt = f"""Az alábbiakban bemutatom a Google (GOOGL) részvény árfolyamadatait az elmúlt 1 hónapra:
{price_data_str}

Elemezd az adatokat röviden, és jósold meg a következő nap záró árfolyamát. Indokold meg röviden a jóslásod főbb okait!
"""

# Modell inicializálása (például gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# Kérés küldése a modellnek
response = model.generate_content(prompt)
print("Predikció és elemzés:")
print(response.text)
