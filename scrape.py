#! /usr/bin/env python3

import logging

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import re
import sys
from time import sleep


PATH_TO_PHANTOM = "/usr/bin/phantomjs"

NW6_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22%7BtqyH%7Cq%5E~Nnk%40kJnaAjDvn%40uLr%5DuYaGkCibAt%40sa%40jMoUtMuA~Beu%40%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"

LOGGER_TAG = "FlatScrape object"


class MissingPageError(Exception):

    def __init__(self):
        pass


class FlatScrape():

    def clean_url(self, dirty_url):
        """ Removes all promotional and unneccessary attributes from the URL """
        clean_url = dirty_url.split("?")[0]
        return clean_url

    def __init__(self, url_to_flat, timeout=30, implicit_wait=20):
        """ 
        Given a URL to a flat description and optional timeout and 
        implicit_wait params, creates an object for parsing the page. 
        The order of parsing is important. First get the monthly_rate and 
        description from first page, then switch to the Location tab 
        to get the longitude and latitude. 
        The only public method is get_flat_info(), returns the dictionary.
        """
        self.logger = logging.getLogger(LOGGER_TAG)
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        driver = webdriver.PhantomJS(executable_path=PATH_TO_PHANTOM)
        driver.set_page_load_timeout(timeout)
        driver.implicitly_wait(implicit_wait)
        driver.maximize_window()
        self.url = self.clean_url(url_to_flat)
        driver.get(self.url)
        self.driver = driver

    def _get_flat_coordinates(self):
        try:
            self.logger.info("Trying to find and click the locationTab")
            self.driver.find_element_by_id("locationTab").click()
            sleep(5)
        except:
            self.logger.error("Failed to find locationTab")

        link = self.driver.find_element_by_xpath(
            """//*[@title="Click to see this area on Google Maps"]""").get_attribute("href")
        self.logger.info("Extracted URL: {}".format(link))
        chars_at_start = "?ll="
        chars_at_end = "&"
        coordinates = link.split(chars_at_start)[1].split(chars_at_end)[0]
        self.logger.info("Coordinates are {}".format(coordinates))
        return coordinates

    def _get_monthly_rate(self):
        full_text_price = self.driver.find_element_by_id(
            "propertyHeaderPrice").text
        monthly_rate = 0
        re_pattern = r"(\d?,?\d{3}) pcm"
        re_exp = re.compile(re_pattern, re.IGNORECASE | re.UNICODE)
        match = re.search(re_exp, full_text_price)
        if match:
            monthly_rate = int(match.group(1).replace(",", ""))
            self.logger.info(
                "Extracted {} as monthly_rate".format(monthly_rate))
        else:
            self.logger.error(
                "No matching regex in {}".format(full_text_price))

        return monthly_rate

    def _get_desciption(self):
        try:
            self.logger.info("Trying to find and extract description section")
            description = self.driver.find_element_by_id("description").text
        except:
            self.logger.error("Couldn't find a Description section")
            pass
        return description

    def get_flat_info(self):
        res = {}
        res["URL"] = self.url
        res["rent"] = self._get_monthly_rate()
        res["description"] = self._get_desciption()
        res["coordinates"] = self._get_flat_coordinates()
        return res


def main():
    test_flat = "http://www.rightmove.co.uk/property-to-rent/property-59802910.html"
    test_flat_fail = "http://www.rightmove.co.uk/property-to-rent/property-65749053.html"
    f = FlatScrape(test_flat)
    print(f.get_flat_info())

if __name__ == "__main__":
    main()
