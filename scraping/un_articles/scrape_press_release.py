import requests
from bs4 import BeautifulSoup

def scrape_press_release(url):
    # Define headers to simulate a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send a GET request to the press release page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parse the press release page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title from the <h1> tag without class filtering
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Title not found"

        # Extract the date from the <p> tag with specific class
        date_tag = soup.find('p', class_='text-xs leading-tight opacity-50 mt-12 lg:mt-2')
        date = date_tag.text.strip() if date_tag else "Date not found"

        # Extract content from all <p> tags and join them into one big string
        p_tags = soup.find_all('p')
        content = '\n'.join([p.text.strip() for p in p_tags])

        # Print the extracted information
        print(f"Title: {title}")
        print(f"Date: {date}")
        print(f"Content: {content}")

        # Return the extracted information
        return {
            'title': title,
            'date': date,
            'content': content,
        }

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Test the function with the given URL
# press_release_url = "https://afghanistan.un.org/en/261118-un-reports-staggering-us-4029-million-recovery-needs-following-last-year%E2%80%99s-earthquakes-herat"
# scrape_press_release(press_release_url)
