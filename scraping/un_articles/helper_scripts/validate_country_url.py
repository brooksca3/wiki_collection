import requests
import json
from tqdm import tqdm
from .input_un_urls import input_un_urls  # Use relative import

def validate_country_urls(urls):
    invalid_text = "The requested page could not be found."
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for url in tqdm(urls, desc="Checking URLs"):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                if invalid_text in response.text:
                    results.append((url, "Invalid"))
                else:
                    results.append((url, "Valid"))
            else:
                results.append((url, "Invalid"))
        except requests.exceptions.RequestException as e:
            results.append((url, f"Invalid (Error: {e})"))

    # Save valid URLs to a JSON file
    valid_urls = [url for url, status in results if status == "Valid"]

    with open('valid_urls.json', 'w') as f:
        json.dump(valid_urls, f)

    return valid_urls

# If you want to run this script independently
if __name__ == "__main__":
    validate_country_urls(input_un_urls)