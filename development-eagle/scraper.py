import requests
import time
import mysql.connector as connector
from bs4 import BeautifulSoup as bs
from bs4 import Comment
from selenium import webdriver
import datetime
import re
import output
import urllib.parse as urlparse

# utility function to remove html tags from page source
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

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

    output.output_data(parameters, db_connection)
        

def scrape_driver(current_url, parameters, url_visited, url_queue, db_connection):
    
    print("Opening driver for: " + current_url)

    # Step 1. Create driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get(current_url)

    # Step 2. Scrape html from current driver before looking for any dynamic changes
    original_html = driver.page_source

    original_soup = bs(original_html, "html.parser")

    scrape_helper(current_url, parameters, original_soup, original_html, db_connection)
    
    add_neighboring_pages(current_url, original_soup, url_visited, url_queue, parameters)

    # Step 3. Enter while loop and check for changes in HTML until time is up
    count = 0

    while (count < int(parameters['time'])):

        print("Searching for any dynamic webpage change at this url..." + str(count + 1))

        newer_html = driver.page_source

        if (original_html != newer_html):

            # Step 4. Scrape the newly found dynamic data.
            new_soup = bs(newer_html, "html.parser")
            
            scrape_helper(current_url, parameters, new_soup, newer_html, db_connection)
            
            add_neighboring_pages(current_url, new_soup, url_visited, url_queue, parameters)
            
            original_html = newer_html

        # Allow one second between each check
        count+=1
        time.sleep(1)

        # Refresh the driver
        driver.refresh()

    # Quit driver as we are done scraping this current url
    driver.quit()


# Adds new urls that have not been visited before to the queue
def add_neighboring_pages(current_url, soup_html, url_visited, url_queue, parameters):
    
    linked_urls = find_neighboring_pages(current_url, soup_html)

    # Update url_queue if any additional neighboring websites are found
    for url in linked_urls:
        
        # Make sure url matches domain currently visiting
        if url not in url_visited:
            
            domain = urlparse.urlparse(url).netloc

            # Check if domain pattern matches found URL
            if domain == parameters["domain"] or domain.split(':')[:1] == parameters["domain"]:
                
                print("Found new url at: " + current_url)

                url_queue.append(url)
                url_visited.append(url)


# Finds all embedded urls within an HTML page
def find_neighboring_pages(current_url, soup_html):
    
    found_urls = []

    a_tags = soup_html.find_all('a')

    for a_tag in a_tags:   
        found_urls.append(a_tag.get('href'))
    
    return found_urls

# Helper function used to call text extractor for the current page
def scrape_helper(current_url, parameters, soup, html, db_connection):

    # 1. Scrape and clean comments from soup
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))

    for comment in comments:

        text_extractor(current_url, parameters, comment, db_connection)
        comment.extract()
    
    # 2. Scrape

    text = remove_html_tags(html)
    text_extractor(current_url, parameters, text, db_connection)



def text_extractor(current_url, parameters, text, db_connection):

    for keyword in parameters['keywords']:
        find_keyword(current_url, keyword, text, db_connection, parameters)

    if parameters['phone']:
        find_phone(current_url, text, db_connection, parameters)

    if parameters['social']:
        find_social(current_url, text, db_connection, parameters)

    if parameters['email']:
        find_email(current_url, text, db_connection, parameters)


def find_keyword(current_url, keyword, text, db_connection, parameters):

    # ignore case sensitive
    for i in re.finditer(keyword.lower(), text.lower()):

        data_insertion_helper(current_url, [keyword], "KEYWORD", db_connection, parameters)


def find_social(current_url, text, db_connection, parameters):

    socials = re.findall(r'(?!219-09-9999|078-05-1120)(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}', text)

    if len(socials) > 0:

        data_insertion_helper(current_url, socials, "SSN", db_connection, parameters)
   

def find_phone(current_url, text, db_connection, parameters):

    phone_numbers = re.findall(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}', text)
  
    if len(phone_numbers) > 0:

        data_insertion_helper(current_url, phone_numbers, "Phone", db_connection, parameters)

def find_email(current_url, text, db_connection, parameters):

    emails = re.findall(r'[a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+', text)

    if len(emails) > 0:

        data_insertion_helper(current_url, emails, "Email", db_connection, parameters)



# Creates a data dictionary for inserting into database  
def data_insertion_helper(current_url, value_list, value_type, db_connection, parameters):

    for value in value_list:
        
        data = {
            'source': current_url,
            'value':  value,
            'type': value_type
        }

        database_insert(data, db_connection, parameters)

            
def database_insert(data, db_connection, parameters):
    try:
        cursor = db_connection.cursor()
        
        now = datetime.datetime.now()

        cursor.execute("INSERT INTO data_table(data_value, data_type, data_source, time_retrieved) values(%s, %s, %s, %s)",
                   (data['value'], data['type'], data['source'], now))

        cursor.execute("INSERT INTO processes(process_id, data_id, time_started) values(%s, %s, %s)",
                    (parameters['process_id'], cursor.lastrowid, parameters['time_started']))        
        
        db_connection.commit()

        cursor.close()

        print("DATA FOUND... inserting into DB.")
    except Exception as e:
        print("data was found... but insertion failed" + str(e))
    
    
    

    
