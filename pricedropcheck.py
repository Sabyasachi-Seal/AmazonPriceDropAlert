import bs4
import urllib.request
import csv
from datetime import datetime
import sendemail

# https://www.amazon.in/Xbox-Wireless-Controller-Robot-White/dp/B08K3GW17S
def get_url(url):
    url = input("Enter the URL of the product: ")
    response = str(requests.get(url)).split(" ")
    while response[1] != "[200]>":
        print("Invalid URL. Try Again.")
        url = input("Enter the URL of the product: ")
        response = str(requests.get(url)).split(" ")
    return url

def save_price(price_list):
    field = ['Time', 'Price']
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = [[dt_string, str(price_list)]]
    with open("prices.csv", 'w') as price_file:
        writer = csv.writer(price_file)
        writer.writerow(field)
        writer.writerows(data)

def price(url):
    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")
    try:
        prices = float(soup.find(class_="a-offscreen").get_text().replace("₹", "").replace(",", ""))
    except AttributeError():
        prices = float(soup.find(class_="a-price-whole").get_text().replace(",", "").replace(".", ""))
    cpmpare(price)
    save_price(price)

def price_alert(price):
    message = f"The Price of the item you were looking for has now dropped to {price}"
    sendemail.send_email(message, sender_email, sender_password, receiver_email)

def compare(price):
    with open("prices.csv", "r") as price_file:
        reader = csv.reader(price_file)
        price_list = []
        for row in reader:
            price_list.append(row)
        price_list = price_list[-2]
        old_price = price_list[-1]
        old_price_time = price_list[-2]
        if old_price>price:
            price_alert(price)

compare(100)