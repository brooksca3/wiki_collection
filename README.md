# Wikipedia AI Detection 📄🤖 (repo in the progress!)

**Detecting AI-Generated Content in Wikipedia Articles**

This repo provides collection and evaluation code for **"Detecting AI-Generated Content in Wikipedia Articles,"** by **Creston Brooks, Samuel Eggert, and Denis Peskoff**. Presented at **NLP for Wikipedia @ EMNLP 2024**.

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

