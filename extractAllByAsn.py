import re
import requests
import sys

def fetch_ip_ranges(asn):
    # URL to fetch the HTML content from the specific ASN page
    url = f"https://bgp.he.net/{asn}#_prefixes"
    
    # Fetch the HTML content using requests
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text

        # Regular expression to match IP ranges in the format like: /net/41.223.56.0/22
        ip_pattern = r'<a href="/net/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})">'

        # Find all matches of the pattern in the HTML content
        ip_matches = re.findall(ip_pattern, html_content)

        # Print and save the matched IP ranges to a text file
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
    else:
        print(f"Failed to retrieve the URL for {asn}. Status code: {response.status_code}")

def process_asns(asns):
    for asn in asns:
        fetch_ip_ranges(asn.strip())

if __name__ == "__main__":
    # Check if the user provided enough arguments
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <asn> or <file_with_asns>")
        sys.exit(1)

    # Check if the argument is a file or an ASN
    input_arg = sys.argv[1]

    try:
        # If the argument is a file, read the ASNs from the file
        with open(input_arg, "r") as file:
            asns = file.readlines()
            process_asns(asns)
    except FileNotFoundError:
        # If the argument is not a file, treat it as a single ASN
        fetch_ip_ranges(input_arg)
