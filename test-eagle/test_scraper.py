import requests
import re
import time
import mysql.connector as connector
from bs4 import BeautifulSoup as bs

# Scrapes our test website
def test_scrape():

    time.sleep(3)
    try:

        data = requests.get('http://127.0.0.1:5000')

        soup = bs(data.text, "html.parser")

        header = soup.find_all('h1')

        print(header[0].text)
    
    except:

        print("unable to reach site")

# Initializes a database connection to our development db container
def test_db_connection():

    try:
        cnx = connector.connect(user='root', password='eagle1234', host='localhost', database='EAGLEEYE')

        print("Database Connection Successful")

        return True
    except:

        return False

    

if __name__ == "__main__":

    # If able to connect to development db, start test scraping
    if test_db_connection():

        test_scrape()
    else:

        print("Database connection failed, unable to scrape")

    
#User-defined queries functions
def get_phone_number():
	count_numbers = 0
	if  [[ $1 == "-p"]]: # argument order may change, just draft   	
        		
	user_defined_phone = $2
	pattern = "/^(?:\(\d{3}\)|\d{3}-)\d{3}-\d{4}$/"  # Phone regex to ensure user input matches phonenumber format
	
	match = re.match(pattern, user_defined_phone)
	if match:
		links = soup.find_all('a')

		for link in links:
    			print(link)# would print urls not ip addresses, not sure how to do this recursively
		
	else:
		break 	 
#add line for count and ip addresses to database
def get_email_addresses():
        count_emails = 0
        if  [[ $3 == "-e"]]: # argument order may change, just draft
    
        user_defined_email = $4
        pattern = '([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)' 

        match = re.match(pattern, user_defined_email)
        if match:
                links = soup.find_all('a')

                for link in links:
                        print(link)# would print urls not ip addresses, not sure how to do this recursively

        else:
                break  
def get_ssns():
	count_ssns = 0
        if  [[ $5 == "-s"]]: # argument order may change, just draft
    
        user_defined_ssn = $6
        pattern = '^\d{3}-\d{2}-\d{4}$'

        match = re.match(pattern, user_defined_ssn)
        if match:
                links = soup.find_all('a')

                for link in links:
                        print(link)# would print urls not ip addresses, not sure how to do this recursively

        else:
                break                                              
