#! /usr/bin/env python3

import logging


NW6_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22%7BtqyH%7Cq%5E~Nnk%40kJnaAjDvn%40uLr%5DuYaGkCibAt%40sa%40jMoUtMuA~Beu%40%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"

KGX_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22wcryH~jUzoAtAjJvdAmx%40n%7D%40iUhR_NixAnA%7D_A%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"

VICTORIA_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22aaiyH~k%5DyDgr%40kDkcAjQ_Jvb%40e%5BjR%7Cf%40uS%7Ct%40sh%40%7C_A%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"

searches = [NW6_SEARCH_URL, KGX_SEARCH_URL, VICTORIA_SEARCH_URL]


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info("importing relevant modules")

    logging.info("Scraping")
    for search_url in searches:
        for url in get_list_of_flats(search_url):
            try:
                f = FlatScrape(url)
                response = f.get_flat_info()
                if response:
                    try:
                        f = DirectionsFromFlat(response["coordinates"])
                        dir_dict = f.get_directions()
                        response.update(dir_dict)
                        pprint.pprint(response)
                    except:
                        pass
            except:
                logging.error("Couldn't scrape {}".format(url))
                pass

if __name__ == "__main__":
    from directions import *
    from scrape import *
    from sheets import WSheet
    main()
