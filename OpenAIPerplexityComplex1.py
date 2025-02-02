from openai import OpenAI
import sys
import json
import time

class PerplexityClient:
    def __init__(self, api_key):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )

    def stream_response(self, messages, model="sonar-pro", max_tokens=1000):
        try:
            response_stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=max_tokens
            )
            
            full_response = ""
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    sys.stdout.write(content)
                    sys.stdout.flush()
            
            print("\n")  # Új sor a válasz végén
            return full_response
        except Exception as e:
            print(f"Hiba történt: {e}")
            return None

    def get_citations(self, response):
        try:
            citations = json.loads(response.model_dump_json())["choices"][0]["message"]["citations"]
            return citations
        except:
            return []

    def interactive_chat(self):
        conversation = []
        print("Kezdjük a beszélgetést! (Kilépéshez írd be: 'exit')")
        
        while True:
            user_input = input("Te: ")
            if user_input.lower() == 'exit':
                break
            
            conversation.append({"role": "user", "content": user_input})
            
            start_time = time.time()
            print("Perplexity: ", end="")
            response = self.stream_response(conversation)
            end_time = time.time()
            
            if response:
                conversation.append({"role": "assistant", "content": response})
                citations = self.get_citations(response)
                
                print(f"\nVálaszidő: {end_time - start_time:.2f} másodperc")
                if citations:
                    print("Források:")
                    for i, citation in enumerate(citations, 1):
                        print(f"{i}. {citation['url']}")
            
            print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    API_KEY = "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"
    perplexity = PerplexityClient(API_KEY)
    perplexity.interactive_chat()
