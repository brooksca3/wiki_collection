import os
import requests
from bs4 import BeautifulSoup
from valid_urls import valid_urls

# Define headers to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_press_release_info(url):
    try:
        # Send a GET request to the press release page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parse the press release page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title and content of the press release
        title = soup.find('h1').text.strip()
        content = '\n'.join([p.text.strip() for p in soup.find_all('p')])

        return title, content

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while accessing {url}: {e}")
        return None, None

def scrape_all_pages(base_url, output_file):
    page = 0
    total_press_releases = 0

    with open(output_file, 'w', encoding='utf-8') as file:
        while True:
            # Construct the URL for the current page
            page_url = f"{base_url}?page={page}"
            print(f"Scraping page: {page_url}")

            try:
                # Send a GET request to the current page
                response = requests.get(page_url, headers=headers)
                response.raise_for_status()  # Check if the request was successful

                # Parse the page content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all press release cards
                press_releases = soup.find_all('div', class_='py-7 sm:py-1 px-5 sm:px-8')

                # If no press releases are found, break the loop
                if not press_releases:
                    print("No more press releases found.")
                    break

                for press_release in press_releases:
                    # Extract the date
                    date = press_release.find('div', class_='mt-3 text-gray-500 text-xs').text.strip()

                    # Extract the URL for the press release
                    press_release_url_suffix = press_release.find('a')['href']

                    # Check if the URL is absolute or relative
                    if not press_release_url_suffix.startswith('http'):
                        press_release_url = f'{base_url.split("/en/press-centre/press-releases")[0]}{press_release_url_suffix}'
                    else:
                        press_release_url = press_release_url_suffix

                    # Extract the title and content
                    title, content = extract_press_release_info(press_release_url)

                    if title and content:
                        # Write the extracted information to the file
                        file.write(f"Date: {date}\n")
                        file.write(f"Title: {title}\n")
                        file.write(f"Content: {content}\n")
                        file.write(f"URL: {press_release_url}\n")
                        file.write("\n\n\n\n")

                        # Increment the counter
                        total_press_releases += 1

                page += 1  # Move to the next page

            except requests.exceptions.RequestException as e:
                print(f"An error occurred while accessing {page_url}: {e}")
                break

    # Print summary of the scraping process
    print(f"Total press releases scraped for {base_url}: {total_press_releases}")

# Create a new directory to store all output files
output_dir = 'press_releases'
os.makedirs(output_dir, exist_ok=True)

# Iterate over all valid URLs
for url in valid_urls:
    country_name = url.split("//")[1].split(".")[0]
    output_file = os.path.join(output_dir, f'{country_name}_press_releases.txt')
    print(f"Starting scrape for {country_name}")
    scrape_all_pages(url, output_file)
    print(f"Finished scrape for {country_name}")
    print("\n\n\n")
