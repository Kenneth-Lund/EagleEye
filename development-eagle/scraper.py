import requests
from bs4 import BeautifulSoup as bs

"""
Main function to handle traversing newly found webpages and queing 
them for further processing.

Parameters:
    - parameters: dict containing information what information 
                  will be targeted and how far this process will run.
"""
def start(parameters):

    #Initialize database connection

    # First url that will be passed into the queue.
    initial_url = parameters.initial_url

    # Max number of url the user wants to traverse
    max_level = parameters.max_level
    
    """
    Queue acts as a way to handle the user's recursive option, handles
    adding newly found URLs when traversing web pages. 
    
    If the user has not selected the recursive option, only the first or specified 
    amount of found urls will be removed from the queue and processed.
    """
    url_queue = []

    # Keep track of sites we already visited.
    url_visited = []

    # Keep track of the level in which our search has traversed.
    level = 1
    
    url_queue.append(initial_url)
    url_visited.append(initial_url)

    while url_queue and level <= max_level:

        current_url = url_queue.pop(0)
        
        print("Currently scrapgin at url: [" + current_url + "] at leve: " + level)

        level+= 1
        
        # Extract HTML: prevents calling same url for each schema value
        data = requests.get(current_url)
        html = bs(data.text, "html.parser")

        # Scrape current html based on parameters
        scrape_webpate(current_url, parameters, html)
        
        # Add any new urls found from current webpage
        linked_urls = find_neighboring_pages(current_url)
        
        for url in linked_urls:

            if url not in url_visited:

                url_queue.append(url)
                utl_visited.append(url)

    print("done scraping")


def scrape_webpage(source, parameters, html):

    # Extract HTML: Avoids making multiple requests each time finding a keyword

    for keyword in parameters.keywords:

        get_keyword(source, parameters, html)

    # If any of these parameters are used, search the current url for it
    if parameters.email: get_email(source, parameters, html)
    if parameters.phone: get_phone(source, parameters, html)
    if parameters.ssn:   get_phone(source, paramaters, html)
    
# Searches for all emails or specified email
def get_email(source, parameters, html):

    print("finding emails")

def get_phone(source, parameters, html):

    print("finding emails")

def get_ssn(source, parameters, html):

    print("finding social")

# Tries to find a keyword on passed in URL
def get_keyword(source, parameters, html):

    print("finding keywords")

def find_neighboring_pages(current_url, html):

    return ["url1", "url2"]
