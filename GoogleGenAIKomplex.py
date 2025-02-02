import os
import google.generativeai as genai

# Győződj meg róla, hogy a GOOGLE_API_KEY be van állítva a környezeti változóban,
# vagy add meg közvetlenül a kulcsot itt:
genai.configure(api_key="AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04")
# Alternatív megoldás: genai.configure(api_key="A_TE_API_KULCSOD")

# Few-shot példa: Kisebb szöveg, ami megmutatja a kívánt kimenet stílusát és tartalmát
few_shot_example = """Példa válasz:
Adatok:
2023-08-01: 150.00
2023-08-02: 152.00
2023-08-03: 151.50

Elemzés:
Az adatsor enyhe növekedést és korrekciót mutat. A piaci aktivitás mérsékelt.

Előrejelzés:
A következő nap záróára valószínűleg 153-155 dollár között lesz.
Indoklás:
A trendek alapján az árfolyam enyhén emelkedhet, figyelembe véve az aktuális piaci hangulat.
"""

# Kérjünk be egy tetszőleges ticker szimbólumot a felhasználótól
ticker_symbol = input("Add meg a részvény tickerét (pl. AAPL): ").upper()

# Itt a részvény adataihoz külső forrást (például yfinance) is használhatnád;
# példaadatként létrehozunk egy mintaszöveget:
price_data = "2023-08-01: 150.00\n2023-08-02: 152.00\n2023-08-03: 151.50\n2023-08-04: 153.00"

# A végső prompt összeállítása:
prompt = f"""
Te egy részvényelemző AI vagy, aki szakmailag precíz, tömör választ ad, és minden kérésre a következő módon reagál:
- Részletesen elemzi az adott részvény árfolyam adatsorát.
- Megadja a legfontosabb észrevételeket, trendeket.
- Jóslatot készít a következő nap záró árfolyamára, indokolva azt.

Néhány példa a kívánt válaszstruktúrára:
{few_shot_example}

Most nézd meg a {ticker_symbol} részvény alábbi árfolyamadatait:
{price_data}

Kérlek, elemezd az adatokat, és add meg:
"""

# Modell inicializálása (például gemini-1.5-flash)
model = genai.GenerativeModel("gemini-1.5-flash")

# Kérés küldése a modellnek az elemzéshez
response = model.generate_content(prompt)

print("\nElemzés és előrejelzés:")
print(response.text)
