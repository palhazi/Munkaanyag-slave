import google.generativeai as genai

# API kulcs beállítása
genai.configure(api_key='AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04')

# Modell kiválasztása
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Kérés küldése
response = model.generate_content("Írj egy rövid verset a tavaszról.")

# Válasz kiírása
print(response.text)



