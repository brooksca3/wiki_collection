import requests
from bs4 import BeautifulSoup

# Define the URL for the country's homepage
homepage_url = "https://afghanistan.un.org/en/press-centre/press-releases"

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

try:
    # Send a GET request to the homepage
    response = requests.get(homepage_url, headers=headers)
    response.raise_for_status()  # Check if the request was successful

    # Parse the homepage content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all press release cards
    press_releases = soup.find_all('div', class_='py-7 sm:py-1 px-5 sm:px-8')

    # List to store all extracted information
    all_press_releases = []

    for press_release in press_releases:
        # Extract the date
        date = press_release.find('div', class_='mt-3 text-gray-500 text-xs').text.strip()

        # Extract the URL for the press release
        press_release_url_suffix = press_release.find('a')['href']

        # Check if the URL is absolute or relative
        if not press_release_url_suffix.startswith('http'):
            press_release_url = f'https://afghanistan.un.org{press_release_url_suffix}'
        else:
            press_release_url = press_release_url_suffix

        # Extract the title and content
        title, content = extract_press_release_info(press_release_url)

        if title and content:
            # Store the extracted information
            press_release_data = {
                'date': date,
                'title': title,
                'content': content,
                'url': press_release_url
            }
            all_press_releases.append(press_release_data)

    # Print all extracted press releases
    for pr in all_press_releases:
        print(f"Date: {pr['date']}")
        print(f"Title: {pr['title']}")
        print(f"Content: {pr['content']}")
        print(f"URL: {pr['url']}")
        print("\n\n\n\n")

    # Optionally, save the data to a file or database

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
