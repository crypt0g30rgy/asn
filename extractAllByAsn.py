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

def fetch_ip_ranges(asn):
    url = f"https://bgp.he.net/{asn}#_prefixes"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {asn}: {e}")
        return

    html_content = response.text
    # Regex to match IP ranges like 41.223.56.0/22
    ip_pattern = r'<a href="/net/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})">'
    ip_matches = re.findall(ip_pattern, html_content)

    if ip_matches:
        file_name = f"ip_ranges_{asn}.txt"
        with open(file_name, "w") as file:
            print(f"\nIP ranges found for {asn}:")
            for ip in ip_matches:
                print(ip)
                file.write(ip + "\n")
        print(f"IP ranges saved to {file_name}")
    else:
        print(f"No IP ranges found for {asn}.")

def process_asns(asns):
    for asn in asns:
        asn = asn.strip()
        if asn:
            fetch_ip_ranges(asn)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <asn> | <asn1,asn2,...> | <file_with_asns>")
        sys.exit(1)

    input_arg = sys.argv[1]

    # Handle comma-separated ASNs
    if ',' in input_arg:
        asns = input_arg.split(',')
        process_asns(asns)
    else:
        try:
            # Try reading as a file
            with open(input_arg, "r") as file:
                asns = file.readlines()
                process_asns(asns)
        except FileNotFoundError:
            # Treat as single ASN
            fetch_ip_ranges(input_arg)
