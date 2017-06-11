## Cortlandt

Scraper of rental flats on offer in specific areas. 


### Requirements

  * pygsheets and a Google Sheet setup
  * Key to Google Maps API
  * Docker - I run this as a container
  * googlemaps, pysheets, selenium from pip
  * phantomjs 


### Design

sheets.py has the WSheet class, which holds the API sign in logic and wrappers around the pygsheets API.

directions.py - DirectionsFromFlat and coord\_tuple\_to_str method. Each scraped flat's coordinates is used to instantiate a new DirectionsFromFlat object. DirectionsFromFlat exposes get\_directions(), which returns a dictionary of results for the given flat. 

scrape.py - FlatScrape object and separate get\_list\_of_flats method. The class and method each have a separate instance of phantomjs webdriver.

run.py - ties it together to scrape and upload new flats and update current flats.


#### Name

Named after the housing project designed by Howard Roark.

#### Thanks

Greg (deployment), Stefano (idea and tip-off)
