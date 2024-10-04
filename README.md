# Wiki AI Detection

**Detecting AI-Generated Content in Wikipedia Articles**

This repository accompanies the paper **"Detecting AI-Generated Content in Wikipedia Articles,"** authored by **Creston Brooks, Samuel Eggert, and Denis Peskoff**. The paper has been accepted for inclusion in the **NLP for Wikipedia Workshop at EMNLP 2024**.

## Repository Overview

This repository provides all the necessary code and data used for detecting AI-generated content in Wikipedia articles. Below is an overview of the main directories and their contents:

### Data Collection (`scraping/`)

The `scraping/` directory contains the code used to collect Wikipedia articles for our study. The scripts allow you to gather recent Wikipedia content for evaluation and analysis. This code was instrumental in collecting the dataset used in our research, particularly articles from August 2024.

### Collected Data and Miscellaneous Scripts (`misc/`)

For convenience, we provide the collected JSON files corresponding to the Wikipedia articles we gathered and evaluated in August 2024. These files are available in the `misc/` directory. In addition to the JSON files, this directory also contains miscellaneous scripts that we used for various data analysis tasks. These scripts are useful for anyone interested in exploring or extending our analysis.

### Evaluation Code (`eval/`)

The `eval/` directory includes code for evaluating AI-generated content using two different tools: **Binoculars** and **GPTZero**. Below are more details on how to use each tool:

- **`binoculars/`**: This directory contains evaluation code for using the Binoculars tool. To use it, you will need to add the [Binoculars GitHub repository](https://github.com/ahans30/Binoculars) as a submodule. This can be done with the following command:

  ```bash
  git submodule add https://github.com/ahans30/Binoculars eval/binoculars
