import scraper
import argparse
import time
import mysql.connector as connector

def main():
    
    parameters = {}

    parser = argparse.ArgumentParser(description='parser for EagleEye')
    parser.add_argument('--url', action='store')

    # Allocated time a website will be scraped for
    parser.add_argument('--time', action='store')

    parser.add_argument('--keywords', action='append')
    
    # store_true will set default to false. if -r is specified, default will change to true
    parser.add_argument('-r', action='store_true') 

    # parse arguments
    args = parser.parse_args()

    if args.r == True:
        parameters["max_level"] = 10000
    else:
        parameters["max_level"] = 1
    
    parameters["time"] = args.time
    parameters["initial_url"] = args.url
    parameters["keywords"] = args.keywords

    start(parameters)

# Recursively calls database until it is ready
def start(parameters):

    try:
        db_connection = connector.connect(user='test', password='test', host='localhost', database='EAGLEEYE')

        scraper.scrape(parameters, db_connection)

    except:

        time.sleep(5)
        print("Database down, trying to connect...")
        start(parameters)


if __name__ == "__main__":
    main()
