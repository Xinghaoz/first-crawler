# first-crawler
My first crawler for crawling the fashion items in "http://www.mogujie.com/" and "http://www.meilishuo.com/".

## Features
+ Language: Python
+ Using Scrapy + Splash
+ Docker

## TODO
- [x] URL
- [x] product title
- [ ] brand (If applicable)
- [ ] categories (If applicable)
- [x] Images (maximum quality) for each color of the product. (Half done, only one)
- [x] Availability for each color and size combination. (Half done, only one)
- [ ] For new product, it can be updated every 6 hours.
- [x] For existing products, we need to update the availability very often (how can you optimize/reduce the delay between a product is out of stock and when our system is aware of that).
- [x] It is understandable that websites change all the time, we need to be notified when crawler failed on some site or some pages, so engineers can investigate and fix the issues.
- [x] If for some reason the crawler restarted, it can recover from where it left off and continue to crawl products / update products.

## USAGE
For running the crawler:
- `scrapy crawl first_crawler`

For running the quantity checker:
- `scrapy crawl quantity_checker`

Before running the crawler we need to set up Splash in Docker:
- `docker run -p 8050:8050 scrapinghub/splash`

You will then need to set the SPLASH_URL setting in your project’s settings.py:
- `SPLASH_URL = 'http://localhost:8050/'`

Don’t forget, if you are using boot2docker on OS X, you will need to set this to the IP address of the boot2docker virtual machine, e.g.:
- `docker-machine ip`
If it shows:
- `192.168.99.100`

Then in settings.py:
- `SPLASH_URL = 'http://192.168.99.100:8050/'`

## Install dependencies
Install MongoDB API of python:
- `python -m pip install pymongo`
