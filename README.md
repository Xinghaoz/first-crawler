# first-crawler
My first crawler writing in python, using Scrapy.

## Features
+ Using Scrapy + Splash
+ Autoupdating every 6 hours

## TODO
- [ ] Basic product information, such as
1. URL
2. product title
3. [x] brand (If applicable)
[x] 4. categories (If applicable)
- [ ] Images (maximum quality) for each color of the product.
- [ ] Availability for each color and size combination.
- [ ] For new product, it can be updated every 6 hours.
- [ ] For existing products, we need to update the availability very often (how can you optimize/reduce the delay between a product is out of stock and when our system is aware of that).
- [ ] It is understandable that websites change all the time, we need to be notified when crawler failed on some site or some pages, so engineers can investigate and fix the issues.
- [ ] If for some reason the crawler restarted, it can recover from where it left off and continue to crawl products / update products.
