#! /usr/bin/env python3

from time import sleep

import logging

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import re

PATH_TO_PHANTOM = "/usr/bin/phantomjs"

NW6_SEARCH_URL = "http://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22%7BtqyH%7Cq%5E~Nnk%40kJnaAjDvn%40uLr%5DuYaGkCibAt%40sa%40jMoUtMuA~Beu%40%22%7D&maxPrice=1750&minBedrooms=2&maxBedrooms=2&viewType=LIST"


class MissingPageError(Exception):

    def __init__(self):
        pass


class FlatScrape():

    def clean_url(self, dirty_url):
        """ Removes all promotional and unneccessary attributes from the URL """
        clean_url = dirty_url.split("?")[0]
        return clean_url

    def __init__(self, url_to_flat, timeout=30, implicit_wait=20):
        driver = webdriver.PhantomJS(executable_path=PATH_TO_PHANTOM)
        driver.set_page_load_timeout(timeout)
        driver.implicitly_wait(implicit_wait)
        driver.maximize_window()
        driver.get(url_to_flat)
        self.driver = driver
        self.flat_url = self.clean_url(url_to_flat)

    def _get_flat_coordinates(self):
        self.driver.find_element_by_id("locationTab").click()
        sleep(5)
        link = self.driver.find_element_by_xpath(
            """//*[@title="Click to see this area on Google Maps"]""").get_attribute("href")
        chars_at_start = "?ll="
        chars_at_end = "&"
        coordinates = link.split(chars_at_start)[1].split(chars_at_end)[0]
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
        else:
            # log failure to find monthly_rate
            pass

        return monthly_rate

    def _get_desciption(self):
        try:
            description = self.driver.find_element_by_id("description").text
        except:
            pass
        return description

    def get_flat_info(self):
        res = {}
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
