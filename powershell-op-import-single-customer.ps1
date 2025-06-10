# Check if a JSON file argument is provided
param (
    [string]$JsonFile
)

# Prompt if no JSON file is provided
if (-not $JsonFile) {
    $JsonFile = Read-Host "Enter the full path to the customer JSON file"
}

# Check if the file exists
if (-Not (Test-Path $JsonFile)) {
    Write-Host "Error: JSON file not found: $JsonFile" -ForegroundColor Red
    exit
}

# Authenticate with 1Password CLI (ensure user is signed in)
$opCheck = op account list 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: 1Password CLI is not signed in. Run 'op signin' first." -ForegroundColor Red
    exit
}

# Extract the vault name from the JSON file
$VaultName = (Get-Content -Raw $JsonFile | ConvertFrom-Json).name
Write-Host "Processing vault: $VaultName" -ForegroundColor Cyan

# Check if the vault exists
$vaultExists = op vault get "$VaultName" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating vault: $VaultName"
    op vault create "$VaultName"
} else {
    Write-Host "Vault already exists: $VaultName"
}

# Set permissions for the vault
Write-Host "Setting permissions for: $VaultName"
op vault user grant --vault "$VaultName" --user "admin@example.com" --permissions view_items,edit_items,create_items,delete_items,view_and_copy_passwords,manage_vault
op vault group grant --vault "$VaultName" --group "Administrators" --permissions view_items,edit_items,create_items,delete_items,view_and_copy_passwords,manage_vault
op vault group grant --vault "$VaultName" --group "support staff" --permissions view_items,edit_items,view_and_copy_passwords,manage_vault

# Read the JSON items
$Items = (Get-Content -Raw $JsonFile | ConvertFrom-Json).items

foreach ($item in $Items) {
    $Title = $item.title
    $ItemJson = $item | ConvertTo-Json -Depth 10 -Compress

    Write-Host "Adding item: $Title to vault $VaultName" -ForegroundColor Green

    # Create a temporary JSON file
    $TempFile = [System.IO.Path]::GetTempFileName()
    $ItemJson | Out-File -FilePath $TempFile -Encoding utf8

    # Use Get-Content to pipe JSON into the op command
    Get-Content -Raw $TempFile | op item create --vault "$VaultName" --format json

    # Remove the temp file
    Remove-Item $TempFile -Force
}

Write-Host "✅ Import complete for vault: $VaultName!" -ForegroundColor Cyan
exit 0
