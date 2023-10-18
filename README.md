# PaperScrape
Repository for scraping pdfs

# TODO
generate pipeline for scraping target polymer data from articles
- system prompts
- questions

Select output data structure for scraped data
- will affect generation

# Install
Python 3.11

```
git clone git@github.com:lopez-hector/PaperScrape.git
cd PaperScrape
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Running Scrape.py
```
python -m src.scrape
```
This will open a chat interface, with an answer to the initial questions and able to receive follow up questions.


