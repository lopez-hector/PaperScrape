# PaperScrape
Repository for scraping pdfs

# TODO
generate pipeline for scraping target polymer data from articles
- system prompts
- questions

Select output data structure for scraped data
- will affect generation

# Install
### Python
Python 3.11
### Terminal
For correct color generation I recommend installing [iterm2.com](https://iterm2.com) terminal.

### Code
```
git clone git@github.com:lopez-hector/PaperScrape.git
cd PaperScrape
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Running Scrape.py
This will open a chat interface, with an answer to the initial questions and able to receive follow up questions.
```
python -m src.scrape
```


## Chat Control
1. submit an input by ending with `//` and then pressing the return key
   2. ```User: Hello //``` press return after `//`
   3. Pressing return without the `//` allows for multiline input
   4. Once you terminate with `//` you will have to wait for the response to come back from the LLM.
2. Exit with `quit` followed by return
   3. ``User: quit`` press return
3. Copy last LLM response to clipboard
   4. ```User: copy//```

