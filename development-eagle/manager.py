import scraper
import argparse
import urllib.parse as urlparse
import time
import datetime
import random
import mysql.connector as connector

def main():
    
    parameters = {}

    parser = argparse.ArgumentParser(description='parser for EagleEye')
    parser.add_argument('--url', action='store')

    # Filename arguement, creates tag for output files
    parser.add_argument('--filename', action='store')

    # Output arguement, for different kinds of output
    parser.add_argument('--output', nargs = '+', default =[])

    # Allocated time a website will be scraped for
    parser.add_argument('--time', action='store')

    parser.add_argument('--keywords', nargs = '+', default =[])
    
    # Recursive arguement
    parser.add_argument('-r', action='store_true') 

    # Scraping priority arguements (s SSN, p Phone, e Email)
    parser.add_argument('-p', action='store_true') 
    parser.add_argument('-s', action='store_true') 
    parser.add_argument('-e', action='store_true') 

    # Parse user arguements for scraping
    args = parser.parse_args()

    if validate_arguements(args):
        
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
        parameters["filename"] = args.filename
        
        # Create unique process ID and time started parameters here
        parameters["process_id"] = createRandomID()
        parameters["time_started"] = datetime.datetime.now()

        # Add initial URL domain to parameters to avoid scraping unknown websites
        domain = str(urlparse.urlparse(args.url).netloc)

        if ":" in domain:
            parameters["domain"] = domain.split(':')[:1]
        else:
            parameters["domain"] = domain

        
        # Add output arguements
        parameters["detail"] = []
        parameters["stat"] = False

        for arg in args.output:

            # NOTE: Case sensitive values for these keys
            if arg.lower() == "phone":
                parameters["detail"].append("Phone")
            
            if arg.lower() == "ssn":
                parameters["detail"].append("SSN")

            if arg.lower() == "email":
                parameters["detail"].append('Email')

            if arg.lower() == "keyword":
                parameters["detail"].append('KEYWORD')
            
            if arg.lower() == "stat":
                parameters["stat"] = True

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


def validate_arguements(args):

    if args.url is None:
        print("No url arguement is given. Please try again.")
        return False
    if args.time is None:
        print("No time arguement is given. Please try again.")
        return False
    if len(args.output) > 6:
        print("Too many arguements given for statistics.")
        return False
    for arg in args.output:
        print(arg)
        if arg.lower() == "stat" or arg.lower() == "phone" or arg.lower() == "ssn" or arg.lower() == "email" or arg.lower() == "keyword":
            pass
        else:
            print(arg + " does not exist for the output arguement. Please try: stat, keyword, phone, ssn, or email")
            return False

    return True

# Generates a random 4 digit number
def createRandomID():

    return str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))



if __name__ == "__main__":
    main()
