import bs4
import requests
import tkinter
import os
import urllib.request
import csv
from datetime import datetime

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

def compare(price):
    with open("prices.csv", "r") as price_file:
        print()