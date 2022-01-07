import bs4
import requests
import tkinter
import os
import urllib.request

# https://www.amazon.in/Xbox-Wireless-Controller-Robot-White/dp/B08K3GW17S
url = input("Enter the URL of the product: ")
sauce = urllib.request.urlopen(url).read()
soup = bs4.BeautifulSoup(sauce, "html.parser")
prices = int(soup.find(class_="a-price-whole").get_text().replace(",", "").replace(".", ""))
print(prices)