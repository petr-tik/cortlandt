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
    parser.add_argument("rent", type=int,
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
            args.rent, args.bedrooms))
    return new_search_urls


def get_old_and_new_flats(search_urls, wks):
    """ 
    Input:
        WSheet object
        search_urls - array of URLs 

    """
    old_flats = list(wks.get_flats().keys())
    new_flats = []
    for search_url in search_urls:
        for flat_url in get_list_of_flats(search_url):
            if flat_url not in old_flats:
                new_flats.append(flat_url)
    return old_flats, new_flats


def upload_new_flats(wks, new_flat_urls):
    """
    Input:
        WSheet object to keep connection with the Google Sheet
        flat_urls - array of flat URLs that aren't in the Worksheet yet

    Output:
    None

    Constructs the full dictionary response and uploads to the worksheet.
    """
    for flat_url in new_flat_urls:
        try:
            f = FlatScrape(flat_url)
            response = f.get_flat_info()
            if response:
                try:
                    f = DirectionsFromFlat(response["coordinates"])
                    dir_dict = f.get_directions()
                    response.update(dir_dict)
                    wks.upload_flat(response)
                except:
                    logging.exception(
                        "Failed to calculate directions for {}".format(flat_url))
        except:
            logging.exception("Couldn't scrape {}".format(flat_url))
            pass


def update_old_flats(wks, flat_urls):
    """
    Input:
        WSheet object to keep connection with the Google Sheet
        flat_urls - array of flat URLs that are already in the Worksheet

    Output:
    None
    """
    pass


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)

    logging.info("Scraping")
    wks = WSheet()
    args = prepare_args()
    searches = prepare_searches(args)

    flats_to_update, flats_to_upload = get_old_and_new_flats(searches, wks)
    upload_new_flats(wks, flats_to_upload)
    update_old(wks, flats_to_update)


if __name__ == "__main__":
    from directions import coord_tuple_to_str, DirectionsFromFlat
    from scrape import get_list_of_flats, FlatScrape
    from sheets import WSheet
    main()
