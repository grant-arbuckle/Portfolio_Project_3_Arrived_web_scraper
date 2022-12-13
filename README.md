# Portfolio Project 3: Arrived web scraper

## Through this project, I learned how to navigate html to build a web scraper to automate the collection of listing data from arrivedhomes.com!
#### - I was looking at my financial picture and wanted to diversify my investments, so I decided to pursue real estate. I found Arrived, which is a company that allows investors to purchase shares of rental properties while avoiding the involved legal aspect of property ownership
#### - Using the selenium library in Python, I built a bot to collect links to all the listings on the Arrived Homes website, then used it to scrape useful information off of each of the listings
#### - Vacation Rentals contain slightly different web pages than single-family-home listings, so I had to scrape the data from those differently, as you can see in the Arrived_scraper.py script
#### - Once the listing data is scraped from both listing types, it is combined and saved in a pandas dataframe, which is output in its raw form to an excel or csv file to be used in future analysis
#### - If a listing is already fully funded/sold out, it is not scraped again. Only unique instances of listings are contained in the output
#### - A demonstration of this web scraper can be seen on my LinkedIn, pinned in the "featured" section: linkedin.com/in/grant-arbuckle-142258174/
