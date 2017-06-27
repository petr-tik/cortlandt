#! /usr/bin/env python3

import json
import logging


import pygsheets
from pygsheets import *
from requests.exceptions import ConnectionError
from datetime import date


class WSheet(pygsheets.Worksheet):

    def __init__(self, worksheet_id=None):
        logging.basicConfig(filename="app.log", level=logging.DEBUG)
        self.logger = logging.getLogger("Flat hunter bot")
        self.logger.info("Trying to connect and authorise")
        try:
            authorised = pygsheets.authorize(
                service_file='./app/service_creds.json')
            self.logger.info("Connected and authorised")
            self.connected = True
        except ConnectionError:
            self.logger.error("Couldn't connect and authorise")
            self.connected = False
        if worksheet_id == None:
            with open("./app/g_sheets_creds.json") as f:
                data = json.load(f)
                self.worksheet_id = data["G_SHEETS_ID"]
        else:
            self.worksheet_id = worksheet_id
        gc = authorised.open_by_key(self.worksheet_id)
        self.flat_wks = gc.worksheet_by_title("flats")
        self.rent_wks = gc.worksheet_by_title("rents")

    def find_header(self):
        """
        Header will always be top row.

        Why this method:
        way to insert the right fields into the right cells. 
        Allows users to rearrange columns manually.

        Returns header array, where the string at index idx 
        is the column name of the column idx.
        """
        row = 1
        header = self.flat_wks.get_row(row)
        return header

    def upload_flat(self, flat_res):
        """
        Input:
            - flat result dictionary
        Returns nothing and inserts row to worksheet
        """
        row = self._prepare_row_for_upload(flat_res)
        self.flat_wks.insert_rows(self.flat_wks.rows, values=row, inherit=True)

    def _prepare_row_for_upload(self, flat_res, header=None):
        """
        Input:
            - flat_result dictionary key: value 

        Returns:
            - array of strings converted to utf-8 
             (fully complaint with http request spec) with errors replaced.
        Selects the correct cell for each key and returns a row
        """
        if header == None:
            header = self.find_header()
        row = []
        for idx, item in enumerate(header):
            if item in ["Date_added", "Date_updated"]:
                continue
            item_to_add = flat_res[item]
            if isinstance(item_to_add, bytes):
                item_to_add = item_to_add.decode(
                    encoding="utf-8", errors="replace")
            row.append(item_to_add)
        date_added = date.today().strftime("%d-%m-%Y")
        # add date added for the update function
        row.append(date_added)
        return row

    def get_flats(self):
        """ 
        Used for updating current flats in run.py. Finds and returns 
        dictionary of flats in the flats worksheet. 
        Returns a dictionary with dictionary as values. 
            key: flat url
            value: another dictionary 
                    with Rent_monthly, Date_added and Date_updated keys and respective string values.
        """
        res = {}
        top_left_idx = (2, 1)
        bottom_right_idx = (self.flat_wks.rows, self.flat_wks.cols)
        values_as_rows = self.flat_wks.get_values(
            top_left_idx, bottom_right_idx, include_all=True)

        header = self.find_header()
        flat_idx = header.index("Flat_link")
        rent_idx = header.index("Rent_monthly")
        date_added_idx = header.index("Date_added")
        date_updated_idx = header.index("Date_updated")

        for flat in values_as_rows:
            res[flat[flat_idx]] = {"Rent_monthly": flat[rent_idx],
                                   "Date_added": flat[date_added_idx],
                                   "Date_updated": flat[date_updated_idx]
                                   }
        return res


if __name__ == "__main__":
    w = WSheet()
    w.get_flats()
