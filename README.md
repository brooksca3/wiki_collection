# The Rise of AI-Generated Content in Wikipedia 📄🤖

This repo provides collection and evaluation code for **"The Rise of AI-Generated Content in Wikipedia,"** by **Creston Brooks, Samuel Eggert, and Denis Peskoff**. Presented at **[NLP for Wikipedia @ EMNLP 2024](https://aclanthology.org/2024.wikinlp-1.12)**.

### Data Collection (`scraping/`) 🗃️🔍

The `scraping/` directory contains the code used to collect Wikipedia articles, Reddit comments, and UN press releases for our study.

### Collected Data and Miscellaneous Scripts (`misc/`) 📂✨

For convenience, we provide the collected JSON files corresponding to the Wikipedia articles we gathered and evaluated in August 2024. These files are available in the `misc/` directory. This directory also contains miscellaneous scripts that we used for various data analysis tasks.

### Evaluation Code (`eval/`) 🛠️📊

The `eval/` directory includes code for evaluating AI-generated content using the two tools we consider: **Binoculars** and **GPTZero**.

- **`binoculars/`**: This directory contains evaluation code for using the Binoculars tool. To use it, you will need to add the [Binoculars GitHub repository](https://github.com/ahans30/Binoculars) as a submodule. This can be done with the following command:

  ```bash
  git submodule add https://github.com/ahans30/Binoculars eval/binoculars

 It is recommended to use a GPU-enabled environment with enough memory to store the Falcon and Falcon-Instruct models needed for Binoculars to run.

- **`gptzero/`**: To use GPTZero, you will need to obtain your own API key and include it in the script. This file assumes you have already collected Wikipedia data into the expected json format (scraping/wikipedia/recent_wiki_scraper.py)

### Replicating Data Collection

To replicate the data collection process, follow these steps for each category.

#### Wikipedia Articles

To replicate the Wikipedia article collection, navigate to `scraping/wikipedia/` and run `python3 run_wiki_scrape.py`. This script will download the text of the 1000 most recently edited articles on Wikipedia and save it to a file called `scraped_wiki_articles.json`. Please note that this process can take up to 1 hour to complete.

#### UN Press Releases

To replicate the UN press release collection, navigate to `scraping/un_articles/` and run `python3 run_un_scrape.py`. This script will download all available UN press releases to a directory called `press_releases`. Please note that this process can take up to 2 hours to complete.

#### Reddit Comments

To replicate the Reddit comment collection, navigate to `scraping/reddit/` and run `python3 run_reddit_scrape.py`. This script will download a sample of 10000 comments from the kaggle dataset and save them to `scraping/reddit/kaggle_data/sampled_comments.json`. Please note that this process will complete in under 1 minute.

### 📄 Citation

If you find this work useful or want to reference it, please cite:
```bibtex
@inproceedings{brooks-etal-2024-rise,
    title = "The Rise of {AI}-Generated Content in {W}ikipedia",
    author = "Brooks, Creston  and
      Eggert, Samuel  and
      Peskoff, Denis",
    editor = "Lucie-Aim{\'e}e, Lucie  and
      Fan, Angela  and
      Gwadabe, Tajuddeen  and
      Johnson, Isaac  and
      Petroni, Fabio  and
      van Strien, Daniel",
    booktitle = "Proceedings of the First Workshop on Advancing Natural Language Processing for Wikipedia",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.wikinlp-1.12",
    doi = "10.18653/v1/2024.wikinlp-1.12",
    pages = "67--79"
}
```
