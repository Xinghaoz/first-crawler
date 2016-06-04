# first-crawler
My first crawler writing in python, using Scrapy.

## TODO
- [ ] Basic product information, such as URL, product title, brand, categories, if applicable.
- [ ] Images (maximum quality) for each color of the product.
- [ ] Availability for each color and size combination.
- [ ] For new product, it can be updated every 6 hours.
- [ ] For existing products, we need to update the availability very often (how can you optimize/reduce the delay between a product is out of stock and when our system is aware of that).
- [ ] It is understandable that websites change all the time, we need to be notified when crawler failed on some site or some pages, so engineers can investigate and fix the issues.
- [ ] If for some reason the crawler restarted, it can recover from where it left off and continue to crawl products / update products.
