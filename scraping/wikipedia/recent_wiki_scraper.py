import requests
from bs4 import BeautifulSoup
import wikipediaapi
import json
from tqdm import tqdm
import time
import random

def get_recent_articles(url, limit=2000):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    articles = []
    page_count = 0
    while len(articles) < limit:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            time.sleep(10)
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        ul_tag = soup.find('ul', class_='mw-contributions-list')

        if ul_tag is None:
            print("Failed to find the list of articles.")
            break

        for li_tag in ul_tag.find_all('li'):
            a_tag = li_tag.find('a', class_='mw-newpages-pagename')
            if a_tag:
                article_title = a_tag['title']
                article_url = 'https://en.wikipedia.org' + a_tag['href']
                articles.append((article_title, article_url))
                if len(articles) >= limit:
                    break

        page_count += 1
        if page_count % 5 == 0 or len(articles) >= limit:
            print(f"Collected {len(articles)} articles so far...")

        next_link = soup.find('a', class_='mw-nextlink')
        if next_link:
            url = 'https://en.wikipedia.org' + next_link['href']
        else:
            break

        time.sleep(random.uniform(1, 3))  # Random delay between requests

    print(f"Finished collecting {len(articles)} articles.")
    return articles[:limit]

def scrape_wikipedia_article(page_title, wiki_wiki, max_retries=3):
    for attempt in range(max_retries):
        try:
            page = wiki_wiki.page(page_title)
            if not page.exists():
                print(f"Page '{page_title}' does not exist.")
                return None
            return page.text
        except (requests.RequestException, requests.Timeout) as e:
            if attempt < max_retries - 1:
                print(f"Error scraping '{page_title}'. Retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Failed to scrape '{page_title}' after {max_retries} attempts.")
                return None

def main():
    recent_articles_url = 'https://en.wikipedia.org/w/index.php?title=Special:NewPages&offset=&limit=50'
    article_limit = 2000
    print(f"Starting to collect {article_limit} recent articles...")
    articles = get_recent_articles(recent_articles_url, limit=article_limit)
    data = []

    wiki_wiki = wikipediaapi.Wikipedia(
        user_agent='WikipediaScraper (your_email@example.com)',
        language='en',
        timeout=30
    )

    for article_title, article_url in tqdm(articles, desc="Scraping articles"):
        content = scrape_wikipedia_article(article_title, wiki_wiki)
        if content:
            data.append({
                'title': article_title,
                'url': article_url,
                'content': content
            })
        time.sleep(random.uniform(0.5, 1.5))  # Random delay between article scrapes

    with open('scraped_recent_articles.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Scraped data has been saved to 'scraped_recent_articles.json'")

if __name__ == "__main__":
    main()