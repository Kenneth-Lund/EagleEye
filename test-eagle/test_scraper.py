import requests
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

    
    