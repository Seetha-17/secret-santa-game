import sys
from server_client import SecretSantaServerClient, ServerConnectionError

def run_remote_pipeline():
    # Base URL collected directly from your browser's address bar
    RENDER_SERVER_URL = "https://onrender.com"
    
    # Files configured inside your application workspace environment
    CURRENT_YEAR_INPUT_FILE = "employee.csv"
    PREVIOUS_YEAR_HISTORY_FILE = "previous_assignments.csv"

    print("--- Initiating Acme Remote Server Secret Santa Pipeline ---")
    
    # Initialize our API client module instance
    client = SecretSantaServerClient(base_url=RENDER_SERVER_URL)
    
    try:
        # Trigger remote generation via API call
        server_response = client.trigger_generate_assignments(
            current_file=CURRENT_YEAR_INPUT_FILE,
            previous_file=PREVIOUS_YEAR_HISTORY_FILE
        )
        
        # Display the server's structured feedback or data output preview
        print("\n--- Live Server Response Data ---")
        import json
        print(json.dumps(server_response, indent=2))
        
    except ServerConnectionError as conn_error:
        print(f"\n[API Connection Fault] {conn_error}", file=sys.stderr)
    except Exception as general_error:
        print(f"\n[Unexpected Local Runtime Failure] {general_error}", file=sys.stderr)

if _name_ == "_main_":
    run_remote_pipeline()