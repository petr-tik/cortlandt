## Cortlandt

Scraper of rental flats on offer in specific areas. 

### Requirements

  * Google sheet for results
  * Docker - I run this as a container
  * APIs: googlemaps, pysheets, selenium from pip
  * Keys to GoogleMaps and Google Sheets
  * phantomjs 


### Design

The Spareroom search URL keeps all necessary parameters, including the location identifier (as a set of polylines). This combined with spareroom's scrape-friendly robots.txt makes it a good target for scraping. Manually selected and saved the search URLs for areas of interest, 

sheets.py has the WSheet class, which holds the API sign in logic and wrappers around the pygsheets API.

directions.py - DirectionsFromFlat and coord\_tuple\_to_str method. Each scraped flat's coordinates is used to instantiate a new DirectionsFromFlat object. DirectionsFromFlat exposes get\_directions(), which returns a dictionary of results for the given flat. The \_find\_closest\_pool() includes different pools coordinates in its scope, but can override them with another dictionary of swimming pools in the format (name: coordinate\_tuple). 

scrape.py - FlatScrape object and separate get\_list\_of_flats method. The class and method each have a separate instance of phantomjs webdriver, which loads the results page.

run.py:

  * parse CLI args - number of bedrooms and monthly rent
  * prepare search URLs with the given args
  * If flat page can be scraped, enrich its data with information on directions
  * Upload flat to google sheets
  

#### Name

Named after the housing project designed by Howard Roark.

#### Thanks

[Stefano](https://github.com/roastario) idea and advice.
