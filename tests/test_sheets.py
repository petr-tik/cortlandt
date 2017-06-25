import unittest

from sheets import *


class SheetsTestCase(unittest.TestCase):

    def setUp(self):
        self.w = WSheet()
        self.flat_to_upload = []

    def test_length_of_flats_array(self):
        """ Number of flats in the worksheet = number of rows - 1 (header) """
        arr = self.w.get_flats().keys()
        self.assertEqual(len(arr), self.w.flat_wks.rows - 1)

    def test_find_header(self):
        """ Header has the same elements in the same order """
        header = self.w.find_header()
        expected_header = ["Flat_link",	"Rent_monthly",	"Time_Flat_to_pool",
                           "Route_flat_to_pool", "Time_Pool_to_office",
                           "Route_pool_to_office", "Time_Petr_swim_commute",
                           "Time_Petr_norm_commute", "Route_norm_commute",
                           "Time_Julius_to_LSE", "Route_Julius_to_LSE",
                           "Description", "Date_added",	"Date_updated"]
        for idx, header_item in enumerate(header):
            self.assertEqual(header_item, expected_header[idx])

    def test_prepare_row_for_upload(self):
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
