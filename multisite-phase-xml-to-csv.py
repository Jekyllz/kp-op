import xml.etree.ElementTree as ET
import csv

# Load the XML file
xml_file_path = "example_export.xml"  # Change this to your actual file path
csv_file_path = "example_export.csv"  # Output CSV file

# Function to extract customer data
def find_customers(root):
    customers = []

    # Find the "test_customers" or "Single Sites" group, but SKIP processing them
    for main_group in root.iter("Group"):
        main_group_name_elem = main_group.find("Name")
        if main_group_name_elem is not None and main_group_name_elem.text:
            main_group_name = main_group_name_elem.text.strip()

            # Skip "test_customers" and "Single Sites" (they are not actual customers)
            if main_group_name.lower() in ["company keypass", "self-hosted customers"]:
                for customer_group in main_group.findall("Group"):  # Process only sub-groups (actual customers)
                    customer_name_elem = customer_group.find("Name")
                    if customer_name_elem is not None and customer_name_elem.text:
                        customer_name = customer_name_elem.text.strip()

                        # Process environments within the customer group
                        for env_group in customer_group.findall("Group"):
                            env_name_elem = env_group.find("Name")
                            if env_name_elem is not None and env_name_elem.text:
                                env_name = env_name_elem.text.strip()

                                if any(keyword.lower() in env_name.lower() for keyword in ["psp", "pre-production", "production", "developement", "staging"]):
                                    # Process items inside the environment, including those in sub-groups (locations)
                                    for item_group in env_group.findall("Group"):
                                        item_name_elem = item_group.find("Name")
                                        if item_name_elem is not None and item_name_elem.text:
                                            item_name = item_name_elem.text.strip()

                                            # Process sub-groups (locations)
                                            for location_group in item_group.findall("Group"):
                                                location_name_elem = location_group.find("Name")
                                                if location_name_elem is not None and location_name_elem.text:
                                                    location_name = location_name_elem.text.strip()
                                                    full_env_name = f"{env_name} - {location_name}"

                                                    # Process credentials inside the location
                                                    for entry in location_group.findall("Entry"):
                                                        customers.append(extract_credentials(entry, customer_name, full_env_name, item_name))

                                            # Also process credentials outside of sub-groups (directly in environment)
                                            for entry in item_group.findall("Entry"):
                                                customers.append(extract_credentials(entry, customer_name, env_name, item_name))

    return customers


# Function to extract credentials from an entry
def extract_credentials(entry, customer_name, environment, item_name):
    credential = {
        "Customer": customer_name,
        "Environment": environment,
        "Item": item_name,
        "Title": "",
        "Username": "",
        "Password": "",
        "URL": "",
        "Notes": ""
    }

    for string in entry.findall("String"):
        key_elem = string.find("Key")
        value_elem = string.find("Value")
        if key_elem is not None and value_elem is not None and key_elem.text and value_elem.text:
            key = key_elem.text.strip()
            value = value_elem.text.strip()

            if key.lower() == "title":
                credential["Title"] = value
            elif key.lower() == "username":
                credential["Username"] = value
            elif key.lower() == "password":
                credential["Password"] = value
            elif key.lower() == "url":
                credential["URL"] = value
            elif key.lower() == "notes":
                credential["Notes"] = value

    return credential


# Extract information
tree = ET.parse(xml_file_path)
root = tree.getroot()
customers_data = find_customers(root)

# Write to CSV
csv_headers = ["Customer", "Environment", "Item", "Title", "Username", "Password", "URL", "Notes"]

with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(customers_data)

print(f"Customer details successfully saved to {csv_file_path} ✅ (Passwords in plain text)")
