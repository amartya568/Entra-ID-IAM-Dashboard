# Employee IAM - Microsoft Entra ID

Employee Identity and Access Management (IAM) project built using
Microsoft Entra ID, Microsoft Graph API, Python, PowerShell, Flask, and
a web-based administration dashboard.

The project demonstrates employee identity lifecycle management through
Joiner, Mover, and Leaver (JML) workflows.

---

## 1. Project Overview

Employee Identity and Access Management is an important part of
enterprise security.

This project provides a practical IAM solution for managing employee
identities in Microsoft Entra ID.

The system integrates Microsoft Graph API with Python and Flask to
perform common identity lifecycle operations.

The main capabilities include:

- Microsoft Entra ID user management
- Microsoft Entra ID group management
- Employee directory
- Joiner workflow
- Mover workflow
- Leaver workflow
- IAM audit logging
- Flask administration dashboard
- Microsoft Graph API integration
- PowerShell-based IAM administration
- Employee search
- Audit log visualization

---

## 2. Project Objectives

The main objectives of this project are:

1. Automate common employee identity management operations.
2. Demonstrate Microsoft Entra ID integration.
3. Implement Joiner-Mover-Leaver lifecycle workflows.
4. Provide a simple web-based IAM administration dashboard.
5. Maintain an audit trail of IAM operations.
6. Demonstrate Microsoft Graph API usage.
7. Provide a foundation for future IAM automation.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | IAM automation and Microsoft Graph integration |
| Flask | Web-based IAM dashboard |
| Microsoft Entra ID | Identity and access management |
| Microsoft Graph API | User and group operations |
| MSAL | Application authentication |
| PowerShell | IAM administration and testing |
| CSV | IAM audit log storage |
| Git | Version control |
| VS Code | Development environment |

---

## 4. Project Structure

The project uses the following structure:

```text
Employee-IAM-EntraID/
│
├── .venv/
│
├── dashboard/
│   ├── __pycache__/
│   ├── static/
│   ├── templates/
│   └── app.py
│
├── docs/
│   ├── screenshots/
│   └── architecture.md
│
├── powershell/
│   └── iam-management.ps1
│
└── python/
    ├── __pycache__/
    ├── jml/
    │   ├── joiner.py
    │   ├── leaver.py
    │   └── mover.py
    │
    ├── applications.py
    ├── groups.py
    ├── iam_audit_log.csv
    ├── logs.py
    └── users.py