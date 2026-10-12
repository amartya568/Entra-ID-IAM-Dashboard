# Employee Identity & Access Management using Microsoft Entra ID

## 1. Project Overview

This project demonstrates a practical Identity and Access Management (IAM)
environment using Microsoft Entra ID and Microsoft Graph API.

The project simulates common enterprise IAM activities such as:

- User identity management
- Group management
- Enterprise application management
- Audit log monitoring
- Microsoft Graph API automation
- Secure application authentication using MSAL
- Future Joiner-Mover-Leaver (JML) automation

---

## 2. Architecture

```text
                    ┌──────────────────────┐
                    │      IT / IAM Admin  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Microsoft Entra ID │
                    │                      │
                    │  Users               │
                    │  Groups              │
                    │  Applications        │
                    │  Audit Logs          │
                    └──────────┬───────────┘
                               │
                               │ Microsoft Graph API
                               ▼
                    ┌──────────────────────┐
                    │    Python IAM Tools  │
                    │                      │
                    │  users.py            │
                    │  groups.py           │
                    │  applications.py     │
                    │  logs.py             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    IAM Operations    │
                    │                      │
                    │  User Management     │
                    │  Group Management    │
                    │  App Visibility      │
                    │  Audit Monitoring    │
                    └──────────────────────┘
```

---

## 3. Technology Stack

| Component | Technology |
|---|---|
| Identity Platform | Microsoft Entra ID |
| API | Microsoft Graph API |
| Programming Language | Python |
| Authentication | Microsoft Authentication Library (MSAL) |
| Configuration | python-dotenv |
| HTTP Client | Requests |
| Future Dashboard | Flask |
| Automation | Python / PowerShell |
| Version Control | Git / GitHub |

---

## 4. Python Modules

### users.py

Retrieves user information from Microsoft Entra ID using Microsoft Graph API.

Current implementation retrieves:

- User ID
- Display name
- User Principal Name

### groups.py

Retrieves groups from Microsoft Entra ID.

Current implementation retrieves:

- Group ID
- Display name
- Description
- Group types

### applications.py

Retrieves Enterprise Application / Service Principal information.

Current implementation retrieves:

- Application ID
- Display name
- Service principal type

### logs.py

Retrieves directory audit logs from Microsoft Entra ID.

Current implementation retrieves:

- Activity name
- Activity date/time
- Operation result

---

## 5. Authentication Flow

The Python modules use application authentication.

```text
Python Application
        │
        ▼
Microsoft Authentication Library (MSAL)
        │
        ▼
Microsoft Entra ID
        │
        ▼
Access Token
        │
        ▼
Microsoft Graph API
        │
        ▼
IAM Data
```

The application uses:

- Tenant ID
- Client ID
- Client Secret

Sensitive credentials are stored in `.env`.

The `.env` file must never be committed to GitHub.

---

## 6. Microsoft Graph Permissions

The application currently uses read permissions for the IAM monitoring
and inventory modules.

Configured permissions include:

- User.Read.All
- Group.Read.All
- Application.Read.All
- AuditLog.Read.All

These permissions allow the project to retrieve identity, group,
application and audit information from Microsoft Entra ID.

---

## 7. Joiner-Mover-Leaver Model

The project simulates the employee identity lifecycle using the
Joiner-Mover-Leaver (JML) model.

### Joiner

A new employee joins the organization.

Typical IAM activities:

1. Create the employee identity
2. Add required user information
3. Assign appropriate groups
4. Provide required application access
5. Configure authentication requirements

### Mover

An existing employee changes department or role.

Typical IAM activities:

1. Update department or job role
2. Review existing access
3. Remove access that is no longer required
4. Assign new groups
5. Review application access

### Leaver

An employee leaves the organization.

Typical IAM activities:

1. Disable the account
2. Remove unnecessary access
3. Review group membership
4. Review application access
5. Record the activity in audit logs

---

## 8. Security Considerations

This project follows basic security practices:

- Secrets are stored in environment variables.
- The `.env` file is excluded using `.gitignore`.
- Microsoft Graph permissions are reviewed before use.
- Test accounts should be used for IAM lifecycle testing.
- Sensitive tenant information should not be published publicly.

---

## 9. Project Status

### Completed

- [x] Microsoft Entra ID application registration
- [x] MSAL authentication
- [x] Microsoft Graph API connection
- [x] User retrieval
- [x] Group retrieval
- [x] Enterprise application retrieval
- [x] Directory audit log retrieval
- [x] Project architecture documentation
- [x] Security considerations documentation

### Planned

- [ ] Joiner workflow
- [ ] Mover workflow
- [ ] Leaver workflow
- [ ] IAM PowerShell automation
- [ ] Flask IAM dashboard
- [ ] Project screenshots
- [ ] GitHub documentation

---