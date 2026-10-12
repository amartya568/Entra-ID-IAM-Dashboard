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


def run_joiner(user_upn, group_id):

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Find employee
    response = requests.get(
        f"{GRAPH_API}/users/{user_upn}"
        "?$select=id,displayName,userPrincipalName,department,jobTitle",
        headers=headers
    )

    if response.status_code != 200:
        return {
            "success": False,
            "message": "Employee not found.",
            "details": response.text
        }

    user = response.json()

    user_id = user["id"]

    # Add employee to group
    membership_data = {
        "@odata.id": f"{GRAPH_API}/directoryObjects/{user_id}"
    }

    response = requests.post(
        f"{GRAPH_API}/groups/{group_id}/members/$ref",
        headers=headers,
        json=membership_data
    )

    if response.status_code == 204:

        return {
            "success": True,
            "message": "Employee successfully added to the group.",
            "employee": user.get("displayName"),
            "group_id": group_id
        }

    if response.status_code == 400:

        return {
            "success": False,
            "message": "Employee may already be a member of this group.",
            "details": response.text
        }

    return {
        "success": False,
        "message": "Graph API error.",
        "details": response.text
    }


if __name__ == "__main__":

    USER_UPN = "jmltestemployee@amitavahazrahotmail.onmicrosoft.com"

    IT_TEAM_GROUP_ID = "4b5a3e44-f052-4a7f-a114-f31099d2e28c"

    result = run_joiner(
        USER_UPN,
        IT_TEAM_GROUP_ID
    )

    print(result)