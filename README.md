# OnTap

Python-based Slack bot that can be added to Slack channels as an app.  

The OnTap bot uses the Slack api to interact with users. 

Users can request information from East Vancouver Breweries: 
    
    Breweries: 33 Acres, Bomber Brewing, Brassneck, Faculty Brewing, Luppolo, Parallel 49, R&B, and Strange Fellows
    
Users identify a <brewery name> and a command <taps, fills, or products> and OnTap responds with a list of today's taps, beers available for growlers fills, or products available in cans and bottles. 
  
Depending on the formatting of the brewery's website, the back-end for the bot uses one or more of requests and lxml, Selenium Webdriver, and Beautiful Soup to pull the latest on-tap information and then packages it up for delivery to the bot.  

    
