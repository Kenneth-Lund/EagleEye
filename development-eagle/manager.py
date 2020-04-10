import scraper
import argparse


def main():
    
    parameters = {}

    parser = argparse.ArgumentParser(description='parser for EagleEye')
    parser.add_argument('--url', action='store')
    
    # store_true will set default to false. if -r is specified, default will change to true
    parser.add_argument('-r', action='store_true') 

    # parse arguments
    args = parser.parse_args()

    if args.r == True:
        parameters["max_level"] = 10000
    else:
        parameters["max_level"] = 1

    parameters["initial_url"] = args.url

    scraper.scrape(parameters)
    

if __name__ == "__main__":
    main()
