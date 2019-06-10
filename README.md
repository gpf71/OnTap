# OnTap

Python-based Slack bot. 

The OnTap bot uses the Slack api to interact log in to Slack channels as an app and interact with users. 

Users can request information from East Vancouver Breweries: 
    
    Breweries: 33 Acres, Bomber Brewing, Brassneck, Faculty Brewing, Luppolo, Parallel 49, R&B, and Strange Fellows
    
Users identify a <brewery name> and a command <taps, fills, or products> and OnTap responds with a list of today's taps, beers available for growlers fills, or products available in cans and bottles. 
  
The back-end for the bot uses Selenium Webdriver and Beautiful Soup to pull the latest on-tap information from the breweries' websites and then packages it up for delivery to the bot.  

    
