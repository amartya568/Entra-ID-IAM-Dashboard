# Employee IAM Management using Microsoft Graph PowerShell

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Employee IAM Management" -ForegroundColor Cyan
Write-Host " Microsoft Entra ID" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

Write-Host "`nChecking Microsoft Graph PowerShell module..."

if (-not (Get-Module -ListAvailable -Name Microsoft.Graph)) {
    Write-Host "Microsoft Graph module is not installed." -ForegroundColor Yellow
    Write-Host "Run: Install-Module Microsoft.Graph -Scope CurrentUser"
    exit
}

Write-Host "Microsoft Graph module found." -ForegroundColor Green

Write-Host "`nConnecting to Microsoft Graph..."

Connect-MgGraph -Scopes "User.Read.All","Group.Read.All"

Write-Host "Connected successfully." -ForegroundColor Green


# =========================
# USER INVENTORY
# =========================

Write-Host "`n========== USER INVENTORY ==========" -ForegroundColor Cyan

$users = Get-MgUser -All -Property DisplayName,UserPrincipalName,AccountEnabled,Department,JobTitle

Write-Host "Users found: $($users.Count)" -ForegroundColor Green

foreach ($user in $users) {

    Write-Host "$($user.DisplayName) | " `
        "Department: $($user.Department) | " `
        "Job: $($user.JobTitle) | " `
        "Enabled: $($user.AccountEnabled)"
}


# =========================
# GROUP INVENTORY
# =========================

Write-Host "`n========== GROUP INVENTORY ==========" -ForegroundColor Cyan

$groups = Get-MgGroup -All -Property DisplayName,Description,GroupTypes

Write-Host "Groups found: $($groups.Count)" -ForegroundColor Green

foreach ($group in $groups) {

    Write-Host "$($group.DisplayName) | " `
        "Description: $($group.Description)"
}


Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host " IAM inventory completed successfully." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan