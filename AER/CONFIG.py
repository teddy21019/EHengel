# scraping
HEADER = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
DOMAIN_URL = "https://www.jstor.org"
JOURNAL_NAME = 'AER'
URL = DOMAIN_URL + "/journal/amereconrevi"
SCRAPE_DECADES = [1980, 1990, 2000, 2010]
SELECTOR_LOAD_ISSUES = "dt.collapse-arrow"
ISSUE_DATA_ATTR = "data-filter"

