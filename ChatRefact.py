import ollama
from typing import List, Dict

class ChatManager:
    def __init__(self, model_name: str = 'llama3:8b'):
        self.model = model_name 
        
    def generate_response(self, prompt: str) -> str:
        try:
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"
            
    def chat_session(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = ollama.chat(model=self.model, messages=messages)
            return response['message']['content']
        except Exception as e:
            return f"Error in chat session: {str(e)}"

def main():
    chat_manager = ChatManager()
    # Example usage
    response = chat_manager.generate_response('Írj nekem egy verset!')
    print(response)

if __name__ == "__main__":
    main()