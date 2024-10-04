import requests
from input_un_urls import input_un_urls
from tqdm import tqdm

def check_urls(urls):
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
                print(f"URL: {url} - Response Code: {response.status_code}")  # Log response code
                results.append((url, "Invalid"))
        except requests.exceptions.RequestException as e:
            print(f"URL: {url} - Error: {e}")  # Log any request exceptions
            results.append((url, f"Invalid (Error: {e})"))

    return results

# Example usage
urls = input_un_urls

results = check_urls(urls)

for url, status in results:
    print(f"URL: {url} - Status: {status}")
