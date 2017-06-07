# -*- coding: utf-8 -*-
#! /usr/bin/env python3

import logging

import re
import sys
from time import sleep


PATH_TO_PHANTOM = "/usr/bin/phantomjs"

NW6_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22%7BtqyH%7Cq%5E~Nnk%40kJnaAjDvn%40uLr%5DuYaGkCibAt%40sa%40jMoUtMuA~Beu%40%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"

KGX_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22wcryH~jUzoAtAjJvdAmx%40n%7D%40iUhR_NixAnA%7D_A%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"

VICTORIA_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22aaiyH~k%5DyDgr%40kDkcAjQ_Jvb%40e%5BjR%7Cf%40uS%7Ct%40sh%40%7C_A%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

searches = [NW6_SEARCH_URL, KGX_SEARCH_URL, VICTORIA_SEARCH_URL]

PATH_TO_PHANTOM = "/usr/bin/phantomjs"


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
        self.logger = logging.getLogger("FlatScrape")
        logging.basicConfig(level=logging.INFO)
        driver = webdriver.PhantomJS(executable_path=PATH_TO_PHANTOM)
        driver.set_page_load_timeout(timeout)
        driver.implicitly_wait(implicit_wait)
        driver.maximize_window()
        self.url = self.clean_url(url_to_flat)
        driver.get(self.url)
        self.driver = driver

    def _get_flat_coordinates(self):
        """
        Uses the rightmove page structure. 
        locationTab contains a URL to Google StreetView 
        with coordinates embedded in the URL.

        Clicks the locationTab, extracts the href from an element 
        with a given xpath.

        If successful - 
            Returns a tuple of flaot for coordinates 
        Else 
            returns (-1, -1)
        """
        try:
            self.logger.info("Trying to find and click the locationTab")
            self.driver.find_element_by_id("locationTab").click()
            sleep(5)
        except:
            self.logger.error("Failed to find locationTab")
            return (-1, -1)
        try:
            xpath_to_query = """//*[@title="Click to see this area on Google Maps"]"""
            link = self.driver.find_element_by_xpath(
                xpath_to_query).get_attribute("href")
            self.logger.info("Extracted URL: {}".format(link))
            chars_at_start = "?ll="
            chars_at_end = "&"
            coordinates_str = link.split(chars_at_start)[
                1].split(chars_at_end)[0]
            self.logger.info("Coordinates are {}".format(coordinates_str))
            coordinates = tuple([float(item)
                                 for item in coordinates_str.split(",")])
            return coordinates
        except NoSuchElementException:
            self.logger.error("No URL to StreetView link.")
            return (-1, -1)

    def _get_monthly_rate(self):
        """
        Extracts the text of the propertyHeaderPrice element 
        and searches for the compiled regex

        If successful, 
            Returns an int for monthly rent (usually in the 1000 - 2500 range)
        Else 
            swallows exceptions internally and returns -1
        """
        monthly_rate = -1
        element_id = "propertyHeaderPrice"
        try:
            full_text_price = self.driver.find_element_by_id(element_id).text
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
        except NoSuchElementException:
            self.logger.error(
                "Couldn't find the {} element".format(element_id))
        return monthly_rate

    def _get_description(self):
        try:
            self.logger.info("Extracting description from {}".format(self.url))
            description = self.driver.find_element_by_id("description").text
            description = description.encode("utf-8", "replace")
        except:
            self.logger.error("Couldn't find a Description section")
            description = ""
        return description

    def _is_page_valid(self):
        """
        Boolean function to check if the page is valid
        """
        try:
            error_box = self.driver.find_element_by_class_name("block")
            if error_box.text == "We are sorry but we could not find the property you have requested.":
                self.logger.error("{} not a valid page".format(self.url))
                return False
            else:
                self.logger.info("{} exists".format(self.url))
                return True
        except:
            self.logger.info("{} exists".format(self.url))
            return True

    def _save_screenshot(self, fname=None):
        """
        Saves a screenshot of the page to cwd.
        Unless a fname is provided, the screenshot file is called 
        {self.url}.png
        """
        if fname == None:
            fname = self.url.split(".html")[0] + ".png"
        self.driver.save_screenshot(fname)

    def get_flat_info(self):
        """ 
        If the page is valid, a dictionary of result is created and 
        populated by calling other class methods to scrape the page. 
        """
        if self._is_page_valid():
            res = {}
            res["Flat_link"] = self.url
            res["Rent_monthly"] = self._get_monthly_rate()
            res["Description"] = self._get_description()
            res["coordinates"] = self._get_flat_coordinates()
            return res
        return None


def get_list_of_flats(results_list_url, timeout=20, implicit_wait=30):
    """ 
    Takes a url to a list of results of the search, 
    returns a list of flat url to scrape.

    Uses another instance of PhantomJS to scrape every element with     
    class_name = "propertyCard-link"
    """
    logger = logging.getLogger("ListGetter")
    driver = webdriver.PhantomJS(executable_path=PATH_TO_PHANTOM)
    driver.set_page_load_timeout(timeout)
    driver.implicitly_wait(implicit_wait)
    driver.maximize_window()
    driver.get(results_list_url)
    class_name = "propertyCard-link"
    flat_list = []
    try:
        logger.info(
            "Looking for elements with class_name: {}".format(class_name))
        full_list = driver.find_elements_by_class_name(class_name)
        all_hrefs = [x.get_attribute("href") for x in full_list]
        flat_list = set(all_hrefs)
    except:
        logger.error("No {} elements found".format(class_name))
    finally:
        return flat_list
