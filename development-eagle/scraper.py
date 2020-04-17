import requests
import time
import mysql.connector as connector
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import datetime

# Scrapes our test website
def scrape(parameters, db_connection):

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

    # Perform BFS until max level is reached.
    while url_queue and level <= max_level:

        current_url = url_queue.pop(0)
        
        print("Currently scraping at url: [" + current_url + "] at level: " + str(level))

        level+= 1

        # Create a driver for the current html to begin scraping
        scrape_driver(current_url, parameters, url_visited, url_queue, db_connection)
    
    # This is where output file gets called, pass the database connection here as well.
    print("Done scraping")
        



def scrape_driver(current_url, parameters, url_visited, url_queue, db_connection):
    
    print("Opening driver for: " + current_url)

    # Step 1. Create driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(current_url)

    # Step 2. Grab html from current driver
    original_html = driver.page_source

    count = 0

    # Step 3. Enter while loop and check for changes in HTML until time is up
    while (count < int(parameters['time'])):

        newer_html = driver.page_source

        if (original_html != newer_html):

            soup_html = bs(newer_html, "html.parser")
            
            # Step 4. Scrape the newly found data.
            scrape_html(current_url, parameters, soup_html, db_connection)

            # Step 5. Check if there are any new urls to enqueue.
            linked_urls = find_neighboring_pages(current_url, soup_html)

            # Step 6. Update url_queue if any additional neighboring websites are found
            for url in linked_urls:

                if url not in url_visited:

                    url_queue.append(url)
                    url_visited.append(url)
            
            original_html = newer_html

        # Allow one second between each check
        count+=1
        time.sleep(1)

    # Quit driver as we are done scraping this current url
    driver.quit()


def scrape_html(current_url, parameters, soup_html, db_connection):

    find_keywords(current_url, parameters['keywords'], soup_html, db_connection)
    
    
# Finds all embedded urls within an HTML page
def find_neighboring_pages(current_url, soup_html):
    
    found_urls = []

    a_tags = soup_html.find_all('a')

    for a_tag in a_tags:
            
        found_urls.append(a_tag.get('href'))
    
    return found_urls


def find_keywords(current_url, keywords, soup_html, db_connection):

    for keyword in keywords:

        if soup_html.findAll(text=keyword):

            data = data_helper(current_url, keyword, "keyword")

            database_insert(data, db_connection)

# Creates a data dictionary for inserting into database  
def data_helper(current_url, value, value_type):

    data = {
        'source': current_url,
        'value':  value,
        'type': value_type
    }

    return data
            

def database_insert(data, db_connection):
    try:
        cursor = db_connection.cursor()
        
        now = datetime.datetime.now()

        cursor.execute("INSERT INTO data_table(process_id, data_value, data_type, data_source, time_retrieved) values(%s, %s, %s, %s, %s)",
                   ("1", data['value'], data['type'], data['source'], now))
        
        
        db_connection.commit()

        cursor.close()

        print("data was found... inserting")
    except:
        print("data was found... but insertion failed")
    
    
    

    
