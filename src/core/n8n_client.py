import requests
import json
from typing import Dict, Any

class N8NClient:
    def __init__(self, base_url: str = "http://localhost:5678"):
        self.base_url = base_url
        self.webhook_base = f"{base_url}/webhook"
        
    def trigger_workflow(self, webhook_id: str, data: Dict[str, Any]) -> Dict:
        """Trigger n8n workflow via webhook"""
        url = f"{self.webhook_base}/{webhook_id}"
        response = requests.post(url, json=data)
        return response.json() if response.ok else {"error": response.text}
    
    def test_connection(self) -> bool:
        """Test if n8n is reachable"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.ok
        except:
            return False
