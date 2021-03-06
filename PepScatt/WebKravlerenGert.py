import requests
from parsel import Selector
import subprocess


import time
start = time.time()

keywords = ["pepe"]
for keyword in keywords:
    links = list()
    #response = requests.get('https://www.google.dk/search?q=%s&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj0yY76x7vhAhWnMewKHWQFB-sQ_AUIDigB&biw=1474&bih=794&dpr=1.25#imgrc=pAZHo8oo3u32YM:' % keyword)
    response = requests.get('https://rare-pepe.com/')
    selector = Selector(response.text)
    href_links = selector.xpath('//a/@href').getall()
# [ ]
    image_links = selector.xpath('//img/@src').getall()

    print('*****************************href_links************************************')
    print(href_links)
    print('*****************************/href_links************************************')
    print('*****************************image_links************************************')
    print(image_links)
    print('*****************************/image_links************************************')

    with open('pepes.txt', 'w') as f:
        f.writelines(image_links)

    image_links.pop(0)
    p = 0
    for i, link in enumerate(image_links):
        if p < 50:
            url = link
            response = requests.get(url)
            if response.status_code == 200:
                with open(keyword+str(i)+".jpg", 'wb') as f:
                    f.write(response.content)
        p += 1




end = time.time()
print("Time taken in seconds : ", (end-start))