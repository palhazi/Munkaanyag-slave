import google.generativeai as genai
import os

# API kulcs beállítása közvetlenül a kódban (javasolt csak teszteléshez, termék környezetben jobb a környezeti változó használata)
genai.configure(api_key="AIzaSyAjP834a4lMnrFiYHg5Aw087CJ1jUSRq04")

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    # Ha a modelled támogatja a kódfuttatást, így engedélyezheted:
    tools="code_execution"
)

prompt = (
    "Write a Python function called fibonacci that takes an integer n and returns "
    "a list of Fibonacci numbers up to the nth number. After that, call the function "
    "with n=10 and print the result. Ensure all steps and code execution are included."
)

response = model.generate_content(prompt)
print("Generated code and execution output:")
print(response.text)
