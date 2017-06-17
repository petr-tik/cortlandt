#! /usr/bin/env python3

import logging
import argparse


NW6_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22%7BtqyH%7Cq%5E~Nnk%40kJnaAjDvn%40uLr%5DuYaGkCibAt%40sa%40jMoUtMuA~Beu%40%22%7D&maxPrice={0}&minBedrooms={1}&maxBedrooms={1}&viewType=LIST"

KGX_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22wcryH~jUzoAtAjJvdAmx%40n%7D%40iUhR_NixAnA%7D_A%22%7D&maxPrice={0}&minBedrooms={1}&maxBedrooms={1}&viewType=LIST"

VICTORIA_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22aaiyH~k%5DyDgr%40kDkcAjQ_Jvb%40e%5BjR%7Cf%40uS%7Ct%40sh%40%7C_A%22%7D&maxPrice={0}&minBedrooms={1}&maxBedrooms={1}&viewType=LIST"


def prepare_args():
    parser = argparse.ArgumentParser(
        description="Set monthly rent (in GBP) and number of rooms")
    parser.add_argument("bedrooms", type=int,
                        help="number of bedrooms in the flat")
    parser.add_argument("rent_monthly", type=int,
                        help="GBP amount paid monthly. Allowed - 0, MAX_INT with 250 increment")
    return parser.parse_args()


def prepare_searches(args):
    """ 
    Takes 
        search URLs 
        input args 
    Returns:
        Array of search URLs according to args
    """
    searches = [NW6_SEARCH_URL, KGX_SEARCH_URL, VICTORIA_SEARCH_URL]

    new_search_urls = []
    for search_url in searches:
        new_search_urls.append(search_url.format(
            args.rent_monthly, args.bedrooms))
    return new_search_urls


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)

    logging.info("Scraping")
    wks = WSheet()
    scraped_flats = wks.get_flats()

    args = prepare_args()
    searches = prepare_searches(args)
    print(searches)
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

                        wks.upload_flat(response)
                    except:
                        logging.exception(
                            "Calculate directions for {}".format(self.url))

            except:
                logging.exception("Couldn't scrape {}".format(self.url))
                pass

if __name__ == "__main__":
    from directions import *
    from scrape import *
    from sheets import WSheet
    main()
