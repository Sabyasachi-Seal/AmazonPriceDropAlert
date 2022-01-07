import bs4
import requests
import urllib.request
import csv
from datetime import datetime
import time
import sendemail

def get_url():
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

def pricer(url):
    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")
    try:
        price = float(soup.find(class_="a-offscreen").get_text().replace("₹", "").replace(",", ""))
    except AttributeError():
        price = float(soup.find(class_="a-price-whole").get_text().replace(",", "").replace(".", ""))
    return price

def price_alert(price):
    message = f"The Price of the item you were looking for has now dropped to {price}"
    sendemail.send_email(message, sender_email, sender_password, receiver_email)

def compare(price):
    sender_email = input("Enter the Email from which you want to get notified: ")
    sender_password = input("Enter the password of the Email from which you want to get notified: ")
    receiver_email = input("Enter the email to which you want to get notified(can be the same as your sender email): ")
    with open("prices.csv", "r") as price_file:
        reader = csv.reader(price_file)
        price_list = []
        for row in reader:
            price_list.append(row)
        price_list = price_list[-2]
        old_price = price_list[-1]
        if int(old_price)>price:
            price_alert(price, send_email, sender_password, receiver_email)
            return True
        return False

def initfile():
    field = ['0', '0']
    data = [['0', '0']]
    with open("prices.csv", 'w') as price_file:
        writer = csv.writer(price_file)
        writer.writerow(field)
        writer.writerows(data)

def main():
    decrease = False
    while decrease==False:
        initfile()
        url = get_url()
        price = pricer(url)
        decrease = compare(price)
        if decrease == False:
            save_price(price_list)
        time.sleep(60*60*6)

if __name__ == '__main__':
    main()


