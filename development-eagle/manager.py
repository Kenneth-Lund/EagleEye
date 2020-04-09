import scraper
import argparse


def main():
    print("HELLO WE MADE IT")
    parser = argparse.ArgumentParser(description='parser for EagleEye')
    parser.add_argument('--url', action='store')
    
    # store_true will set default to false. if -r is specified, default will change to true
    parser.add_argument('-r', action='store_true') 

    # parse arguments
    args = parser.parse_args()


    if args.r == True:
        print('recursive mode enabled')
    else:
        print('recursive mode disabled')


if __name__ == "__main__":
    main()
