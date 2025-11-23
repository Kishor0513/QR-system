$port = 8080
$ruleName = "Allow Python Web Server (Port $port)"

# Check for Administrator privileges
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requesting Administrator privileges to add firewall rule..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "Adding Firewall Rule: '$ruleName'..." -ForegroundColor Cyan

# Remove existing rule if it exists (to avoid duplicates)
netsh advfirewall firewall delete rule name="$ruleName" | Out-Null

# Add the new rule
netsh advfirewall firewall add rule name="$ruleName" dir=in action=allow protocol=TCP localport=$port

if ($?) {
    Write-Host "Success! Firewall rule added." -ForegroundColor Green
    Write-Host "Port $port is now open for other devices." -ForegroundColor Green
} else {
    Write-Host "Failed to add firewall rule." -ForegroundColor Red
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
