import requests
from bs4 import BeautifulSoup
import json
import re

def get_number_of_footnotes(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return 0

        soup = BeautifulSoup(response.content, 'html.parser')
        footnotes = soup.find_all("li", id=lambda x: x and x.startswith('cite_note-'))
        return len(footnotes)

    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return 0

def count_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return len([s for s in sentences if s.strip()])

def get_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page content. Status code: {response.status_code}")
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = " ".join(p.get_text() for p in paragraphs)
        return content

    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return ""

def process_articles(file_path, output_file='link_updated.json'):
    # List of titles to process, if empty, process all
    # titles_to_process = None
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
        
        num_footnotes = get_number_of_footnotes(url)
        content = get_article_content(url)
        num_sentences = count_sentences(content)
        footnotes_per_sentence = num_footnotes / num_sentences if num_sentences > 0 else 0

        output_data.append({
            'title': title,
            'num_footnotes': num_footnotes,
            'num_sentences': num_sentences,
            'footnotes_per_sentence': footnotes_per_sentence
        })

        print(f"Found {num_footnotes} footnotes and {num_sentences} sentences for article '{title}'. Footnotes per sentence: {footnotes_per_sentence:.2f}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    print(f"Updated data saved to '{output_file}'")

def main():
    file_path = 'it_links.json'
    output_file = 'footnotes_jsons/it/combo_footnotes.json'
    process_articles(file_path, output_file=output_file)

if __name__ == "__main__":
    main()
