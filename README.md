# OnTap

What's available today at the local breweries? 

FRONT END: 

Python-based Slack bot "OnTap" that can be added to Slack channels as an app.  

OnTap uses the Slack api to interact with users, who can request information from East Vancouver Breweries: 
    
    33 Acres, Bomber Brewing, Brassneck, Faculty Brewing, Luppolo, Parallel 49, R&B, and Strange Fellows
    
Users identify a <brewery name> and a command <taps, fills, or products>
OnTap responds with a list of today's taps, beers available for growlers fills, or products available in cans and bottles. 

BACK END: 

OnTap.py
OnTap is the main file:  Controls updating of brewery information and report generation.  

Brewery.py 
Creates Brewery objects which store brewery name, short name, url, (date) updated, address, location, logo, and lists of items available on tap, for fills, and in bottles and cans.

BreweryResources.py
Collections of resources such as url for brewery webpages used by the other files. 

BreweryScraper.py 
The brewery websites display "today's taps" and product information in a variety of formats and using different technologies, necessitating a custom update function for each one. BreweryScraper uses one or more of requests and lxml, Selenium Webdriver, and Beautiful Soup to pull the latest on-tap information from each brewery's website and then packages it up for delivery to the bot. Only scrapes a maximum of once per day.

    
TODOs and USER STORIES:

Todo: add breweries: Off the Rail, Powell Street, Postmark  

User story: OnTap bot - add option to request in a single command taps and fills and products (or combination thereof) for a brewery

User story: what's on tap near me? (requires different front end implementation) 
