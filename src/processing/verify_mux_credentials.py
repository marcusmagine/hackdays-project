import os
import requests
from dotenv import load_dotenv

def verify_mux_credentials():
    """Verify Mux API credentials by making a simple API call."""
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")

    # Check if .env file exists
    env_path = os.path.join(os.getcwd(), '.env')
    print(f".env file exists: {os.path.exists(env_path)}")

    # Read .env file directly
    if os.path.exists(env_path):
        print("Reading .env file directly:")
        with open(env_path, 'r') as f:
            env_contents = f.read()
            print(env_contents)

    # Load environment variables
    load_dotenv(override=True)

    # Get credentials from environment
    token_id = os.getenv("MUX_TOKEN_ID")
    token_secret = os.getenv("MUX_TOKEN_SECRET")

    # Print the exact values (be careful with secrets in production)
    print(f"MUX_TOKEN_ID value: '{token_id}'")
    print(f"MUX_TOKEN_SECRET value: '{token_secret}'")

    if not token_id or not token_secret:
        print("Error: Mux credentials not found in environment variables.")
        return False

    # Make a simple API call to verify credentials
    try:
        response = requests.get(
            "https://api.mux.com/video/v1/assets",
            auth=(token_id, token_secret)
        )

        if response.status_code == 200:
            print("Success! Credentials are valid.")
            return True
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    verify_mux_credentials()