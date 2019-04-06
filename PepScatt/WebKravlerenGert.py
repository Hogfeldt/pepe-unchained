import requests
from parsel import Selector

import time
start = time.time()

links = list()
### Crawling to the website

# GET request to recurship site
response = requests.get('https://www.google.dk/search?q=pepe&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj0yY76x7vhAhWnMewKHWQFB-sQ_AUIDigB&biw=1474&bih=794&dpr=1.25#imgrc=pAZHo8oo3u32YM:')

## Setup for scrapping tool

# "response.txt" contain all web page content
selector = Selector(response.text)

# Extracting href attribute from anchor tag <a href="*">
href_links = selector.xpath('//a/@href').getall()


#Extracting src attribute from img tag <img src="*">
image_links = selector.xpath('//img/@src').getall()

print('*****************************href_links************************************')
print(href_links)
print('*****************************/href_links************************************')



print('*****************************image_links************************************')
print(image_links)
print('*****************************/image_links************************************')

with open('pepes.txt', 'w') as f:
    f.write(image_links[1])


end = time.time()
print("Time taken in seconds : ", (end-start))