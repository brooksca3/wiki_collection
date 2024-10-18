import json
import sys
from pathlib import Path

#-----------------------------------------------------------------------
# The script to scrape UN articles, first by validating the country URLs
# and then by scraping the press releases for each country and saving
# them to a "press_releases" directory
#
# Usage: python run_un_scrape.py
#-----------------------------------------------------------------------

# Add the project root directory to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from helper_scripts import validate_country_url as validate
from helper_scripts import scrape_all_press_releases as scrape
from helper_scripts.input_un_urls import input_un_urls

if __name__ == "__main__":
    valid_urls = validate.validate_country_urls(input_un_urls)
    with open('valid_urls.json', 'w') as f:
        json.dump(valid_urls, f)
    print("Valid URLs saved to valid_urls.json")
    print("Saving press releases to press_releases directory")
    scrape.scrape_all_press_releases()