import csv
import json
import os
import re

# Input/Output Files
csv_file_path = "example_export.csv"
json_directory = "example_export"

# Ensure output directory exists
if not os.path.exists(json_directory):
    os.makedirs(json_directory)

# Regex to detect IP addresses
ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

# Function to escape non-password fields
def escape_value(value):
    if not value:
        return ""
    return (
        value.strip()
             .replace("\n", " ")
             .replace("\r", " ")
             .replace("%", "%%")  # Escape % for JSON compatibility
             .replace('"', '\\"')  # Escape "
             .replace("$", "\\$")  # Escape $
    )

# Dictionary to store customer vault data
vaults = {}

# Read CSV and convert to JSON
with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    
    for row in reader:
        customer_name = escape_value(row["Customer"])
        environment = escape_value(row["Environment"])
        item_name = escape_value(row["Item"])
        title = escape_value(row["Title"])
        username = escape_value(row["Username"])
        password = row["Password"].strip()  # DO NOT ESCAPE OR MODIFY PASSWORDS
        url = escape_value(row["URL"])
        notes = escape_value(row["Notes"])

        # Ensure password is never empty
        password = password if password else "semafone"

        # Construct fields properly
        fields = [
            {"id": "username", "label": "Username", "type": "STRING", "value": username},
            {"id": "password", "label": "Password", "type": "CONCEALED", "purpose": "PASSWORD", "value": password},  # RAW, untouched
            {"id": "notesPlain", "label": "Notes", "type": "STRING", "purpose": "NOTES", "value": notes}
        ]

        # Handle URL and IP addresses properly
        if url:
            if ip_regex.match(url):
                fields.append({"id": "ip_address", "label": "IP Address", "type": "STRING", "value": url})
            else:
                fields.append({"id": "url", "label": "URL", "type": "URL", "value": url})

        # Create credential item
        item = {
            "title": f"{title} - {item_name} ({environment})",
            "category": "PASSWORD",
            "version": 1,
            "fields": fields
        }

        # Create vault if not exists
        if customer_name not in vaults:
            vaults[customer_name] = {
                "name": customer_name,
                "description": f"Vault for {customer_name}",
                "attributeVersion": 1,
                "items": []
            }

        vaults[customer_name]["items"].append(item)

# Save JSON with proper escaping for passwords
for customer, vault_data in vaults.items():
    try:
        # Prevent additional escaping by setting ensure_ascii=False
        json_string = json.dumps(vault_data, indent=4, ensure_ascii=False)
        json.loads(json_string)  # Validate JSON
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON validation failed for {customer}: {e}")
        continue  # Skip saving invalid JSON

    # Sanitize filename
    sanitized_name = re.sub(r'[^\w\-_]', '_', customer)
    json_file_path = os.path.join(json_directory, f"{sanitized_name}.json")

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_string)

print(f"✅ 1Password JSON files saved in '{json_directory}/'")
