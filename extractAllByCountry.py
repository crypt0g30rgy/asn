import re
import requests
import sys

# Ensure the user provides the required command-line argument
if len(sys.argv) != 2:
    print("Usage: python script_name.py <country_name>")
    sys.exit(1)

# Get the country name from the command-line argument
country_name = sys.argv[1]

# URL to fetch the HTML content from
url = f"https://bgp.he.net/search?search%5Bsearch%5D={country_name}&commit=Search"

# Fetch the HTML content using requests
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text

    # Regular expression to match IP ranges in CIDR notation
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}\b'

    # Regular expression to match ASNs (e.g., AS12345)
    asn_pattern = r'AS\d+'

    # Find all matches of the patterns in the HTML content
    ip_matches = re.findall(ip_pattern, html_content)
    asn_matches = re.findall(asn_pattern, html_content)

    # Save the matched IP ranges to a text file and print them
    if ip_matches:
        ip_file_name = f"ip_ranges_{country_name}.txt"
        with open(ip_file_name, "w") as ip_file:
            print("IP ranges found:")
            for ip in ip_matches:
                print(ip)
                ip_file.write(ip + "\n")
        print(f"\nIP ranges saved to {ip_file_name}")
    else:
        print("No IP ranges found.")

    # Save the matched ASNs to a text file and print them
    if asn_matches:
        asn_file_name = f"asns_{country_name}.txt"
        with open(asn_file_name, "w") as asn_file:
            print("\nASNs found:")
            for asn in asn_matches:
                print(asn)
                asn_file.write(asn + "\n")
        print(f"\nASNs saved to {asn_file_name}")
    else:
        print("No ASNs found.")
else:
    print(f"Failed to retrieve the URL. Status code: {response.status_code}")
