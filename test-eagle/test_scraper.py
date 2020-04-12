import requests
import time
import mysql.connector as connector
from bs4 import BeautifulSoup as bs

# Scrapes our test website
def test_scrape(parameters):

    #Initialize database connection

    # First url that will be passed into the queue.
    initial_url = parameters['initial_url']

    # Max number of url the user wants to traverse
    max_level = parameters['max_level']
    
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
        
        print("Currently scraping at url: [" + current_url + "] at level: " + str(level))

        level+= 1
        """
        # Extract HTML: prevents calling same url for each schema value
        data = requests.get(current_url)
        html = bs(data.text, "html.parser")

        # Scrape current html based on parameters
        scrape_webpage(current_url, parameters, html)
        
        # Add any new urls found from current webpage
        linked_urls = find_neighboring_pages(current_url, html)
        
        for url in linked_urls:

            if url not in url_visited:

                url_queue.append(url)
                utl_visited.append(url)
        """
    print("done scraping")

def scrape_webpage(source, parameters, html):

    print("Scraping url at: " + source)

def find_neighboring_pages(current_url, html):
    
    urls_found = ["url1", "url2"]
    
    return urls_found


# Initializes a database connection to our development db container
def test_db_connection():

    try:
        cnx = connector.connect(user='test', password='test', host='localhost', database='EAGLEEYE')

        print("Database Connection Successful")

        return True
    except:

        return False

    
if __name__ == "__main__":

    # If able to connect to development db, start test scraping
    if test_db_connection():
        
        parameters = { "initial_url": "http://127.0.0.1:5000", "max_level": 1000}

        test_scrape(parameters)
    else:

        print("Database connection failed, unable to scrape")

    
    