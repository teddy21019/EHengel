# scraping
HEADER = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
DOMAIN_URL = "https://www.jstor.org"
JOURNAL_NAME = 'ECA'
URL = DOMAIN_URL + "/journal/econometrica"
SCRAPE_DECADES = [1950,1960,1970,1980, 1990, 2000, 2010]
SELECTOR_LOAD_ISSUES = "dt.collapse-arrow"
ISSUE_DATA_ATTR = "data-filter"

