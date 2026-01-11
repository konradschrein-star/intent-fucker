"""
Ollama API Client
Handles communication with the local Ollama service
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        
    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def generate(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Send a prompt to Llama 3.1 via Ollama
        Returns the raw text response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for more consistent JSON responses
                "num_predict": 500   # Limit response length
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('response', '').strip()
                else:
                    print(f"Ollama API error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"Request timeout (attempt {attempt + 1}/{max_retries})")
            except Exception as e:
                print(f"Error calling Ollama: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
        
        return None
    
    def parse_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON from Llama's response
        Handles cases where the model includes extra text
        """
        if not response:
            return None
        
        # Try to find JSON in the response
        try:
            # First, try direct parsing
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from text
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end > start:
                try:
                    json_str = response[start:end]
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def generate_json(self, prompt: str, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """
        Generate a response and parse it as JSON
        Returns parsed JSON dict or None if failed
        """
        response = self.generate(prompt, max_retries)
        if response:
            return self.parse_json_response(response)
        return None


# Test function
if __name__ == "__main__":
    client = OllamaClient()
    
    print(f"Ollama available: {client.is_available()}")
    print(f"Available models: {client.list_models()}")
    
    if client.is_available():
        test_prompt = """Respond with valid JSON only: {"status": "ok", "message": "Ollama is working!"}"""
        result = client.generate_json(test_prompt)
        print(f"Test response: {result}")
