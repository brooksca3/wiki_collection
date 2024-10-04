import re
import os
import json
import sys
import argparse
from bino_utils import ai_score

def clean_text(text):
    # Replace all newlines with a unique string
    text = text.replace('\n', '!@#').replace('\t', ' ')
    # Split the text by the unique string
    split_text = text.split('!@#')
    # Remove elements with 5 or fewer words
    split_text = [segment for segment in split_text if len(segment.split()) > 5]
    # Rejoin the text
    text = ' '.join(split_text)
    # Remove "References" and "External links" sections
    text = re.sub(r'== References ==.*|== External links ==.*', '', text, flags=re.DOTALL)
    
    return text.strip()

def extract_title_text_and_url(wikipedia_entries):
    titles = []
    texts = []
    urls = []
    for entry in wikipedia_entries:
        title = entry.get('title', '')
        content = entry.get('content', '')
        url = entry.get('url', '')
        cleaned_text = clean_text(content)
        if title and cleaned_text:
            titles.append(title)
            texts.append(cleaned_text)
            urls.append(url)
    return titles, texts, urls

def process_files(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        wikipedia_entries = json.load(file)
    titles, texts, urls = extract_title_text_and_url(wikipedia_entries)
    texts = [' '.join(text.strip().split()[:400]) for text in texts]
    final_texts, final_titles, final_urls = [],[],[]
    for ind, text in enumerate(texts):
        if len(text.split()) >= 100:
            final_texts.append(texts[ind])
            final_titles.append(titles[ind])
            final_urls.append(urls[ind])

    bino_scores = ai_score(final_texts)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for title, score, url, text in zip(final_titles, bino_scores, final_urls, final_texts):
            outfile.write(f"{title}, {score[0]}, {url}, actual_text_used_for_scoring: {text}\n")

def main():
    parser = argparse.ArgumentParser(description="Process and score Wikipedia entries.")
    parser.add_argument('input_file', type=str, help="Path to the input JSON file in the wiki_jsons directory.")
    args = parser.parse_args()

    input_file = 'wiki_jsons/' + args.input_file
    print(input_file)
    output_file_name = os.path.basename(input_file).replace('.json', '_scored.json')
    output_file = os.path.join('wiki_jsons_scored', output_file_name)

    os.makedirs('wiki_jsons_scored', exist_ok=True)

    process_files(input_file, output_file)

if __name__ == "__main__":
    main()
