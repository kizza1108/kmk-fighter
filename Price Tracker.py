

import requests # this library directs our url
from bs4 import BeautifulSoup # beautiful soup is a library used to extract data from html files
import smtplib
import time
#this is my url for my product#
my_URL = "https://www.amazon.co.uk/Samsung-Galaxy-Fold4-256GB-Renewed/dp/B0BNNMFGR8/ref=sr_1_4?crid=TF2A1TJ7PFIS&keywords=galaxy%2Bz%2Bfold&qid=1703270641&sprefix=galaxy%2Bz%2Bfold%2B%2Caps%2C90&sr=8-4&ufe=app_do%3Aamzn1.fos.23648568-4ba5-49f2-9aa6-31ae75f1e9cd&th=1"

# a user agent is a string that is used to make a request to a HTTP web server to fetch information
headers = {"User-Agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'}
#error occured here with browser where None is returned, just copy user agent from a different browser

def check_price():
    page = requests.get(my_URL, headers=headers) 
    soup = BeautifulSoup(page.content, 'html.parser') # this parses the wbesite to find specific items

    title = soup.find(id ="productTitle").get_text() # in the soup module, it finds this particular product id
    price = soup.find(class_ = "a-price-whole").get_text() #find the specific class

    converted_price = float(price)

    if (converted_price < 700):
        send_mail()

        
    print(title.strip()) 
    print(converted_price)

    if (converted_price < 700):
        send_mail()


def send_mail():
    server =smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo() #used by email server to identify when connecting to another email
    server.starttls()
    server.ehlo()

    server.login('kizzakiran@gmail.com', 'cmqhlmmugozaiykl')

    subject = 'Price fell down!'
    body = 'Check the amazon link https://www.amazon.co.uk/Samsung-Galaxy-Fold4-256GB-Renewed/dp/B0BNNMFGR8/ref=sr_1_4?crid=TF2A1TJ7PFIS&keywords=galaxy%2Bz%2Bfold&qid=1703270641&sprefix=galaxy%2Bz%2Bfold%2B%2Caps%2C90&sr=8-4&ufe=app_do%3Aamzn1.fos.23648568-4ba5-49f2-9aa6-31ae75f1e9cd&th=1'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('kizzakiran@gmail.com','kiran.mahesh.kumar61@gmail.com',msg)

    print('Email sent')

    server.quit()

check_price()

while True:
    check_price()
    time.sleep(3600) # runs and checks the code every hour

