import re
import requests
import sys

# Latest Chrome User-Agent
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

# Ensure the user provides the required command-line argument
if len(sys.argv) != 2:
    print("Usage: python script_name.py <country_name>")
    sys.exit(1)

country_name = sys.argv[1].strip()

# Construct the search URL
url = f"https://bgp.he.net/search?search%5Bsearch%5D={country_name}&commit=Search"

try:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching data for '{country_name}': {e}")
    sys.exit(1)

html_content = response.text

# Regex to match IP ranges (CIDR)
ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}\b'
# Regex to match ASNs
asn_pattern = r'AS\d+'

# Find all matches
ip_matches = sorted(set(re.findall(ip_pattern, html_content)))
asn_matches = sorted(set(re.findall(asn_pattern, html_content)))

# Save IP ranges
if ip_matches:
    ip_file_name = f"ip_ranges_{country_name.lower()}.txt"
    with open(ip_file_name, "w") as ip_file:
        print(f"\nIP ranges found for {country_name}:")
        for ip in ip_matches:
            print(ip)
            ip_file.write(ip + "\n")
    print(f"\nIP ranges saved to {ip_file_name}")
else:
    print(f"No IP ranges found for {country_name}.")

# Save ASNs
if asn_matches:
    asn_file_name = f"asns_{country_name.lower()}.txt"
    with open(asn_file_name, "w") as asn_file:
        print(f"\nASNs found for {country_name}:")
        for asn in asn_matches:
            print(asn)
            asn_file.write(asn + "\n")
    print(f"\nASNs saved to {asn_file_name}")
else:
    print(f"No ASNs found for {country_name}.")
