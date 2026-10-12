import os
import sys
import csv
import requests
import msal

from flask import Flask, render_template, request
from dotenv import load_dotenv


# --------------------------------------------------
# PYTHON PATH
# --------------------------------------------------

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "python"
    )
)

from logs import write_log


# --------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------

load_dotenv()

app = Flask(__name__)


# --------------------------------------------------
# ENTRA ID CONFIGURATION
# --------------------------------------------------

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = (
    f"https://login.microsoftonline.com/{TENANT_ID}"
)

GRAPH_API = "https://graph.microsoft.com/v1.0"

IT_TEAM_GROUP_ID = (
    "4b5a3e44-f052-4a7f-a114-f31099d2e28c"
)


# --------------------------------------------------
# AUDIT LOG PATH
# --------------------------------------------------

AUDIT_LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "python",
    "iam_audit_log.csv"
)


# --------------------------------------------------
# GET ACCESS TOKEN
# --------------------------------------------------

def get_access_token():

    client = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )

    token_response = client.acquire_token_for_client(
        scopes=[
            "https://graph.microsoft.com/.default"
        ]
    )

    return token_response.get("access_token")


# --------------------------------------------------
# GRAPH HEADERS
# --------------------------------------------------

def get_graph_headers():

    access_token = get_access_token()

    if not access_token:
        return None

    return {
        "Authorization": f"Bearer {access_token}"
    }


# --------------------------------------------------
# GET USERS
# --------------------------------------------------

def get_users():

    headers = get_graph_headers()

    if not headers:
        return []

    response = requests.get(
        f"{GRAPH_API}/users"
        "?$select=id,displayName,userPrincipalName,"
        "accountEnabled,department,jobTitle",
        headers=headers
    )

    if response.status_code == 200:
        return response.json().get("value", [])

    print(
        f"Graph users error: "
        f"{response.status_code}"
    )

    return []


# --------------------------------------------------
# GET GROUPS
# --------------------------------------------------

def get_groups():

    headers = get_graph_headers()

    if not headers:
        return []

    response = requests.get(
        f"{GRAPH_API}/groups"
        "?$select=id,displayName,description,groupTypes",
        headers=headers
    )

    if response.status_code == 200:
        return response.json().get("value", [])

    print(
        f"Graph groups error: "
        f"{response.status_code}"
    )

    return []


# --------------------------------------------------
# GET AUDIT LOG
# --------------------------------------------------

def get_audit_logs():

    logs = []

    try:

        if not os.path.exists(
            AUDIT_LOG_FILE
        ):
            return []

        with open(
            AUDIT_LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                logs.append(row)

        logs.reverse()

        return logs

    except Exception as error:

        print(
            f"Audit log read error: {error}"
        )

        return []


# --------------------------------------------------
# JOINER WORKFLOW
# --------------------------------------------------

def run_joiner(user_upn):

    access_token = get_access_token()

    if not access_token:

        write_log(
            "JOINER",
            user_upn,
            "Add employee to IT Team",
            "Authentication failed"
        )

        return "ERROR: Authentication failed."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{GRAPH_API}/users/{user_upn}"
        "?$select=id,displayName,userPrincipalName",
        headers=headers
    )

    if response.status_code != 200:

        write_log(
            "JOINER",
            user_upn,
            "Add employee to IT Team",
            "Employee not found"
        )

        return "ERROR: Employee not found."

    user = response.json()

    membership_data = {
        "@odata.id":
            f"{GRAPH_API}/directoryObjects/{user['id']}"
    }

    response = requests.post(
        f"{GRAPH_API}/groups/"
        f"{IT_TEAM_GROUP_ID}/members/$ref",
        headers=headers,
        json=membership_data
    )

    if response.status_code == 204:

        write_log(
            "JOINER",
            user_upn,
            "Add employee to IT Team",
            "Success"
        )

        return (
            f"SUCCESS: {user['displayName']} "
            f"successfully added to IT Team."
        )

    if response.status_code == 400:

        write_log(
            "JOINER",
            user_upn,
            "Add employee to IT Team",
            "Already member or Graph rejected request"
        )

        return (
            f"INFO: {user['displayName']} may already be "
            f"a member of IT Team."
        )

    write_log(
        "JOINER",
        user_upn,
        "Add employee to IT Team",
        f"Graph API Error: {response.status_code}"
    )

    return (
        f"ERROR: Graph API Error: "
        f"{response.text}"
    )


# --------------------------------------------------
# MOVER WORKFLOW
# --------------------------------------------------

def run_mover(
    user_upn,
    department,
    job_title
):

    access_token = get_access_token()

    if not access_token:

        write_log(
            "MOVER",
            user_upn,
            "Update department and job title",
            "Authentication failed"
        )

        return "ERROR: Authentication failed."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{GRAPH_API}/users/{user_upn}"
        "?$select=id,displayName,userPrincipalName,"
        "department,jobTitle",
        headers=headers
    )

    if response.status_code != 200:

        write_log(
            "MOVER",
            user_upn,
            "Update department and job title",
            "Employee not found"
        )

        return "ERROR: Employee not found."

    user = response.json()

    update_data = {
        "department": department,
        "jobTitle": job_title
    }

    response = requests.patch(
        f"{GRAPH_API}/users/{user['id']}",
        headers=headers,
        json=update_data
    )

    if response.status_code == 204:

        write_log(
            "MOVER",
            user_upn,
            f"Department={department}; "
            f"JobTitle={job_title}",
            "Success"
        )

        return (
            f"SUCCESS: {user['displayName']} "
            f"updated successfully. "
            f"Department: {department}, "
            f"Job Title: {job_title}"
        )

    write_log(
        "MOVER",
        user_upn,
        "Update department and job title",
        f"Graph API Error: {response.status_code}"
    )

    return (
        f"ERROR: Graph API Error: "
        f"{response.text}"
    )


# --------------------------------------------------
# LEAVER WORKFLOW
# --------------------------------------------------

def run_leaver(user_upn):

    access_token = get_access_token()

    if not access_token:

        write_log(
            "LEAVER",
            user_upn,
            "Disable employee account",
            "Authentication failed"
        )

        return "ERROR: Authentication failed."

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{GRAPH_API}/users/{user_upn}"
        "?$select=id,displayName,userPrincipalName,"
        "accountEnabled,department,jobTitle",
        headers=headers
    )

    if response.status_code != 200:

        write_log(
            "LEAVER",
            user_upn,
            "Disable employee account",
            "Employee not found"
        )

        return "ERROR: Employee not found."

    user = response.json()

    update_data = {
        "accountEnabled": False
    }

    response = requests.patch(
        f"{GRAPH_API}/users/{user['id']}",
        headers=headers,
        json=update_data
    )

    if response.status_code == 204:

        write_log(
            "LEAVER",
            user_upn,
            "Disable employee account",
            "Success"
        )

        return (
            f"SUCCESS: {user['displayName']} "
            f"account disabled successfully. "
            f"Status: Leaver completed"
        )

    write_log(
        "LEAVER",
        user_upn,
        "Disable employee account",
        f"Graph API Error: {response.status_code}"
    )

    return (
        f"ERROR: Graph API Error: "
        f"{response.text}"
    )


# --------------------------------------------------
# DASHBOARD DATA
# --------------------------------------------------

def dashboard_data():

    users = get_users()
    groups = get_groups()
    audit_logs = get_audit_logs()

    total_users = len(users)

    active_users = sum(
        1
        for user in users
        if user.get("accountEnabled") is True
    )

    disabled_users = (
        total_users - active_users
    )

    total_groups = len(groups)

    return (
        users,
        groups,
        audit_logs,
        total_users,
        active_users,
        disabled_users,
        total_groups
    )


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/", methods=["GET"])
def dashboard():

    (
        users,
        groups,
        audit_logs,
        total_users,
        active_users,
        disabled_users,
        total_groups
    ) = dashboard_data()

    return render_template(
        "index.html",
        users=users,
        groups=groups,
        audit_logs=audit_logs,
        total_users=total_users,
        active_users=active_users,
        disabled_users=disabled_users,
        total_groups=total_groups,
        message=None
    )


# --------------------------------------------------
# JOINER ROUTE
# --------------------------------------------------

@app.route("/joiner", methods=["POST"])
def joiner():

    user_upn = request.form.get(
        "user_upn",
        ""
    ).strip()

    message = run_joiner(
        user_upn
    )

    (
        users,
        groups,
        audit_logs,
        total_users,
        active_users,
        disabled_users,
        total_groups
    ) = dashboard_data()

    return render_template(
        "index.html",
        users=users,
        groups=groups,
        audit_logs=audit_logs,
        total_users=total_users,
        active_users=active_users,
        disabled_users=disabled_users,
        total_groups=total_groups,
        message=message
    )


# --------------------------------------------------
# MOVER ROUTE
# --------------------------------------------------

@app.route("/mover", methods=["POST"])
def mover():

    user_upn = request.form.get(
        "user_upn",
        ""
    ).strip()

    department = request.form.get(
        "department",
        ""
    ).strip()

    job_title = request.form.get(
        "job_title",
        ""
    ).strip()

    message = run_mover(
        user_upn,
        department,
        job_title
    )

    (
        users,
        groups,
        audit_logs,
        total_users,
        active_users,
        disabled_users,
        total_groups
    ) = dashboard_data()

    return render_template(
        "index.html",
        users=users,
        groups=groups,
        audit_logs=audit_logs,
        total_users=total_users,
        active_users=active_users,
        disabled_users=disabled_users,
        total_groups=total_groups,
        message=message
    )


# --------------------------------------------------
# LEAVER ROUTE
# --------------------------------------------------

@app.route("/leaver", methods=["POST"])
def leaver():

    user_upn = request.form.get(
        "user_upn",
        ""
    ).strip()

    message = run_leaver(
        user_upn
    )

    (
        users,
        groups,
        audit_logs,
        total_users,
        active_users,
        disabled_users,
        total_groups
    ) = dashboard_data()

    return render_template(
        "index.html",
        users=users,
        groups=groups,
        audit_logs=audit_logs,
        total_users=total_users,
        active_users=active_users,
        disabled_users=disabled_users,
        total_groups=total_groups,
        message=message
    )


# --------------------------------------------------
# START DASHBOARD
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )