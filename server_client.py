# server_client.py
import requests
from typing import Dict, Any

class ServerConnectionError(Exception):
    """Raised when the remote server returns an error or is unreachable."""
    pass

class SecretSantaServerClient:
    def _init_(self, base_url: str):
        # Strip any trailing slashes to prevent malformed endpoint routes
        self.base_url = base_url.rstrip('/')

    def trigger_generate_assignments(self, current_file: str, previous_file: str) -> Dict[str, Any]:
        """
        Sends a POST request to the server's /generate-assignments/ endpoint
        with the payload structure displayed on the Swagger/OAS 3.1 UI documentation.
        """
        endpoint = f"{self.base_url}/generate-assignments/"
        
        # Exact payload matched to the request body schema in the image
        payload = {
            "current_year_file": current_file,
            "previous_year_file": previous_file
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            print(f"Connecting to server at: {endpoint}...")
            response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
            
            # Raise an exception automatically for 4xx or 5xx status codes
            response.raise_for_status()
            
            print("Server successfully processed the assignment rules!")
            return response.json()
            
        except requests.exceptions.Timeout:
            raise ServerConnectionError("The connection to the server timed out. Render instances may take a moment to wake up.")
        except requests.exceptions.HTTPError as http_err:
            raise ServerConnectionError(f"Server responded with an HTTP Error: {http_err.response.status_code} - {http_err.response.text}")
        except requests.exceptions.RequestException as e:
            raise ServerConnectionError(f"Failed to connect to the server infrastructure: {e}")