import requests
from bs4 import BeautifulSoup
import json
import re
import argparse

def get_number_of_hyperlinks(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return 0

        soup = BeautifulSoup(response.content, 'html.parser')
        hyperlinks = soup.find_all("a", href=lambda x: x and x.startswith('/wiki/'))
        return len(hyperlinks)

    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return 0

def count_words(text):
    words = re.split(r'\s+', text)
    return len([w for w in words if w.strip()])

def get_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page content. Status code: {response.status_code}")
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get all text, not just paragraphs
        content = soup.get_text(separator=" ")
        return content

    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return ""

def process_articles(file_path, output_file='link_updated.json'):
    # List of titles to process, if empty, process all
    titles_to_process = [] ## add your titles here! e.g., ['Discografia di Gloria Gaynor', 'NGC 874', 'Dragon Ball Side Story: Vita da Yamcha']

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output_data = []

    for article in data:
        title = article['title']
        url = article['url']

        if titles_to_process and title not in titles_to_process:
            continue

        print(f"Processing article: {title}")
        
        num_hyperlinks = get_number_of_hyperlinks(url)
        content = get_article_content(url)
        num_words = count_words(content)
        hyperlinks_per_word = num_hyperlinks / num_words if num_words > 0 else 0

        output_data.append({
            'title': title,
            'num_hyperlinks': num_hyperlinks,
            'num_words': num_words,
            'hyperlinks_per_word': hyperlinks_per_word
        })

        print(f"Found {num_hyperlinks} hyperlinks and {num_words} words for article '{title}'. Hyperlinks per word: {hyperlinks_per_word:.6f}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"Updated data saved to '{output_file}'")

def main():
    parser = argparse.ArgumentParser(description='Scrape recent Wikipedia articles.')
    parser.add_argument('--lang', type=str, default='en', help='Language code for Wikipedia API (e.g., "en" for English, "de" for German).')
    args = parser.parse_args()
    file_path = f'{args.lang}_links.json'
    output_file = f'hyperlinks_jsons/{args.lang}/combo_hyperlinks.json'
    process_articles(file_path, output_file=output_file)

if __name__ == "__main__":
    main()
