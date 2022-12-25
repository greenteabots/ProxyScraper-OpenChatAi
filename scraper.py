import requests
from bs4 import BeautifulSoup
import json

# Set up the API key and search engine ID
API_KEY = "YOUR_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

def search_web(query):
    # Make a request to the Google Search API
    response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}")

    # Parse the JSON response
    results = json.loads(response.text)

    # Return the list of results
    return results["items"]

def get_proxies(url):
    # Make a request to the website that lists free proxies
    response = requests.get(url)

    # Parse the HTML of the website
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all of the rows in the table that contain the proxies
    rows = soup.find("table", {"id": "proxylisttable"}).tbody.find_all("tr")

    # For each row, extract the IP address and port number of the proxy
    proxies = []
    for row in rows:
        columns = row.find_all("td")
        ip_address = columns[0].text
        port = columns[1].text
        proxy = f"{ip_address}:{port}"
        proxies.append(proxy)

    return proxies

def save_proxies(proxies):
    # Open a file for writing
    with open("proxies.txt", "w") as file:
        # Write each proxy to a new line in the file
        for proxy in proxies:
            file.write(proxy + "\n")

# Search the web for websites that list proxies
query = "free proxy list"
results = search_web(query)

# Scrape the websites for proxies
all_proxies = []
for result in results:
    url = result["link"]
    proxies = get_proxies(url)
    all_proxies.extend(proxies)

# Save the proxies to a file
save_proxies(all_proxies)