import google.generativeai as genai

# Állítsd be a saját API kulcsodat
genai.configure(api_key='AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04')

# Válassz egy megfelelő modellt (például a "gemini-1.5-flash" modellt)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Indíts el egy beszélgetési sessiont
chat = model.start_chat()

print("Chat alkalmazás elindítva! Írj be üzenetet ('exit' a kilépéshez).")

while True:
    user_input = input("Te: ")
    if user_input.lower() == "exit":
        print("Kilépés a chatből.")
        break

    try:
        # Üzenet küldése a chat sessionnek, a válasz több részletben is érkezhet
        response = chat.send_message(user_input)
        # A válasz kiírása
        print("Bot:", response.text)
    except Exception as e:
        print("Hiba történt az API hívása során:", e)

