import requests
from bs4 import BeautifulSoup as bs
import time

if __name__ == "__main__":
    
    while(True):

        time.sleep(3)
        try:

            data = requests.get('http://127.0.0.1:5000')

            soup = bs(data.text, "html.parser")

            header = soup.find_all('h1')

            print(header[0].text)
        
        except:

            print("unable to reach site")