from openai import OpenAI
import sys

# Kulcs beállítása
client = OpenAI(
    api_key="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",
    base_url="https://api.perplexity.ai"
)

# Kérés küldése streamelve
response_stream = client.chat.completions.create(
    model="sonar-pro",
    messages=[
        {"role": "system", "content": "Légy pontos és tömör"},
        {"role": "user", "content": "Hány bolygó van a Naprendszerben?"}
    ],
    stream=True
)

# Válasz fogadása és kiírása részletenként
for chunk in response_stream:
    if chunk.choices[0].delta.content is not None:
        sys.stdout.write(chunk.choices[0].delta.content)
        sys.stdout.flush()

print()  # Új sor a válasz végén

