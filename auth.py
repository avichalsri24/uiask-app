import os
import requests

def fetch_orchestrator_token(logger):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get('ORCHESTRATOR_EXTERNAL_APP_ID'),
        'client_secret': os.environ.get('ORCHESTRATOR_EXTERNAL_APP_SECRET'),
        'scope': 'OR.Jobs',
    }

    try:
        response = requests.post('https://staging.uipath.com/identity_/connect/token', headers=headers, data=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        return response.json().get('access_token')
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve orchestrator token: {str(e)}")
        return None
