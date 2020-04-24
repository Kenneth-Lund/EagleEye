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

    parser.add_argument('--keywords', nargs = '+', default =[])
    
    # store_true will set default to false. if -r is specified, default will change to true
    parser.add_argument('-r', action='store_true') 

    parser.add_argument('-p', action='store_true') 
    parser.add_argument('-s', action='store_true') 
    parser.add_argument('-e', action='store_true') 

    # parse arguments
    args = parser.parse_args()

    if args.r == True:
        parameters["max_level"] = 10000
    else:
        parameters["max_level"] = 1

    if args.e == True:
        parameters["email"] = True
    else:
        parameters["email"] = False

    if args.p == True:
        parameters["phone"] = True
    else:
        parameters["phone"] = False

    if args.s == True:
        parameters["social"] = True
    else:
        parameters["social"] = False
    
    parameters["time"] = args.time
    parameters["initial_url"] = args.url
    parameters["keywords"] = args.keywords

    start(parameters)

# Recursively calls database until it is ready
def start(parameters):

    try:
        db_connection = connector.connect(user='test', password='test', host='localhost', database='EAGLEEYE')

        scraper.scrape(parameters, db_connection)

        db_connection.close()
    except:

        time.sleep(5)
        print("Database down, trying to connect...")
        start(parameters)


if __name__ == "__main__":
    main()
