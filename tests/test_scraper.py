import unittest

from scrape import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class TestFlatScrape(unittest.TestCase):

    def setUp(self):
        self.good_page = FlatScrape(
            "file://" + "/app/tests/test_valid_flat.html")
        self.bad_page = FlatScrape(
            "file://" + "/app/tests/test_error_flat.html")

    def test_is_page_valid_fail(self):
        self.assertEqual(False, self.bad_page._is_page_valid())

    def test_is_page_valid_good(self):
        self.assertEqual(True, self.good_page._is_page_valid())

    def test_get_coordinates_exception_on_fail(self):
        self.bad_page._save_screenshot()
        self.assertEqual(self.bad_page._get_flat_coordinates(), (-1, -1))

    def test_get_coordinates_ret_type_on_success(self):
        self.good_page._save_screenshot()
        expected_coords = (51.491127, -0.139348)
        ret = self.good_page._get_flat_coordinates()
        self.assertEqual(expected_coords, ret)

    def test_get_monthly_rate(self):
        ret = self.good_page._get_monthly_rate()
        expected_ret = 1625
        self.assertEqual(ret, expected_ret)

    def test_no_description_on_fail(self):
        self.assertEqual(self.bad_page._get_description(), "")

    def test_description_on_valid_page(self):
        self.assertGreater(len(self.good_page._get_description()), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)

"""
new tork - trash.

CV - interesting.

NYC - greencard

no language pref = C + + is easier,

thinks devs are second - class citizens.

work on quant models,

new, startups.


had an offer from DE Shaw(unspecified quant or dev). Most puzzles were algorithmic.

todo:
two sigma - fomc article
ansatz -
"""
