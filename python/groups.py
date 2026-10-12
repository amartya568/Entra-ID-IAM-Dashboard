import os
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_API = "https://graph.microsoft.com/v1.0"

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

token_response = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" not in token_response:
    print("Authentication failed!")
    print(token_response.get("error"))
    print(token_response.get("error_description"))
    exit()

access_token = token_response["access_token"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    f"{GRAPH_API}/groups?$select=id,displayName,description,groupTypes",
    headers=headers
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    groups = response.json().get("value", [])

    print("\nGroups found:", len(groups))

    for group in groups:
        print(
            f"- {group.get('displayName')} | "
            f"ID: {group.get('id')} | "
            f"{group.get('description') or 'No description'}"
        )
else:
    print("Graph API Error:")
    print(response.text)