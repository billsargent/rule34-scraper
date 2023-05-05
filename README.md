# rule34-scraper
A hacky way to scrape rule34.paheal.net

This code is horrible. It uses beautiful soup to scrape its way through all posts starting at 1. It skips over videos. It inserts into an sqlite database all the information about the image it downloaded including a CRC and the image data itself. And no, you should never store massive amounts of blob binary data in an sqlite db. I did this for fun. 

I'm showing this mainly to help people with beautifulsoup. 
