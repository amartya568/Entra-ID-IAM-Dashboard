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


def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    token_response = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in token_response:
        raise Exception(
            "Authentication failed: "
            + token_response.get("error_description", "")
        )

    return token_response["access_token"]


def run_leaver(user_upn):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Find employee
    response = requests.get(
        f"{GRAPH_API}/users/{user_upn}"
        "?$select=id,displayName,userPrincipalName,"
        "accountEnabled,department,jobTitle",
        headers=headers
    )

    if response.status_code != 200:
        return {
            "success": False,
            "message": "Employee not found.",
            "details": response.text
        }

    user = response.json()

    # Disable employee account
    update_data = {
        "accountEnabled": False
    }

    response = requests.patch(
        f"{GRAPH_API}/users/{user['id']}",
        headers=headers,
        json=update_data
    )

    if response.status_code == 204:
        return {
            "success": True,
            "message": "Employee account disabled successfully.",
            "employee": user.get("displayName"),
            "user_upn": user.get("userPrincipalName"),
            "department": user.get("department"),
            "job_title": user.get("jobTitle"),
            "account": "Disabled",
            "status": "Leaver completed"
        }

    return {
        "success": False,
        "message": "Graph API error.",
        "details": response.text
    }


if __name__ == "__main__":
    USER_UPN = "jmltestemployee@amitavahazrahotmail.onmicrosoft.com"

    result = run_leaver(USER_UPN)

    print(result)