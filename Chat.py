import ollama

# Modell inicializálása (példaként a 'llama2' modellt használjuk)
response = ollama.chat(model='llama3:8b', messages=[
    {
        'role': 'user',
        'content': 'At the moment is Bill Gates married?',
    },
])

# A válasz kiírása
print(response['message']['content'])

