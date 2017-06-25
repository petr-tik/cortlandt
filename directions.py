#! /usr/bin/env/ python3


import googlemaps
from datetime import datetime
import logging
import sys

import pprint


def coord_tuple_to_str(coord_tuple):
    return ",".join(map(str, coord_tuple))


class DirectionsFromFlat():

    def __init__(self, flat_coords):
        """ 
        Input - flat_coords from which all distances will be measured.

        """
        self.logger = logging.getLogger("DirectionsFromFlat")
        self.flat = flat_coords
        cn_office = (51.521120, -0.101294)
        self.office = cn_office
        key = self._get_key()
        try:
            self.logger.info("Trying to connect to Gmaps API")
            self.gmaps = googlemaps.Client(key)
        except:
            self.logger.error("Couldn't connect to the Gmaps API")

    def _get_key(self):
        fname = "./app/g_maps_creds.json"
        try:
            import json
            with open(fname) as f:
                data = json.load(f)
                return data["API_key"]
        except IOError:
            self.logger.error("Couldn't find file {}".format(fname))

    def time_to_finish(self, start, finish, mode, dep_time=datetime.now()):
        """ 
        Input:
        - start coordinates
        - finish coordinates
        - transport mode - either "walking" or "transit"
        - departure time

        Output:
        - Minutes (int) from start to finish with a given mode of transport 
        In case of errors or invalid input, returns 0

        Queries distance_matrix API and returns the number of minutes. 
        Walking is independent of departure time (like transit, 
        where tube times matter), so defaults to now. 

        For transit the solution is to run the deamon at normal time of commute 
        0830 - 0900 
        """
        error_return = 0
        if start == (-1, -1) or finish == (-1, -1):
            self.logger.error(
                "Invalid coordinates: start: {}, finish: {}".format(start, finish))
            return error_return
        if start == None:
            start = self.flat
        self.logger.info(
            "Finding time to {} from {} to {}".format(mode, start, finish))

        try:
            self.logger.info("Request to GMaps Distance Matrix. Mode: \
                              {}, {} -> {}".format(mode, start, finish))
            response = self.gmaps.distance_matrix(
                start, finish, mode=mode, departure_time=dep_time)
            if response['status'] == "OK":
                self.logger.info("Request recieved and parsed successfully")
                seconds = response["rows"][0][
                    "elements"][0]["duration"]["value"]
                return seconds // 60
            else:
                self.logger.error(
                    "Request failed. Response status: {}".format(response["status"]))
                return error_return
        except:
            self.logger.error("API threw exception")
            return error_return

    def time_to_walk(self, finish, start=None):
        if start == None:
            start = self.flat
        return self.time_to_finish(start, finish, mode="walking")

    def time_to_transit(self, finish, start=None):
        if start == None:
            start = self.flat
        return self.time_to_finish(start, finish, mode="transit")

    def _find_closest_pool(self, pools_to_consider=None):
        """ 
        Input:
        - object itself with coordinates

        Output (tuple):
        - coordinates of the pool that's closest to walk to
        - time it takes to walk from flat to closest pool
        """
        pools = {"Swiss Cottage Leisure Centre": (51.542309, -0.172880),
                 "Queen Mother Sports Centre": (51.493335, -0.140532),
                 "Oasis Leisure Centre": (51.515734, -0.125891),
                 "Pancras Square Leisure": (51.533834, -0.126326),
                 "Kentish Town Sports Centre": (51.547039, -0.144027)
                 }
        if pools_to_consider == None:
            pools_to_consider = pools
        min_time = 100  # won't be walking for a hundred minutes
        closest_pool = None
        for key in pools_to_consider:
            time_to_pool = self.time_to_walk(pools_to_consider[key])
            if not closest_pool or time_to_pool < min_time:
                closest_pool = pools_to_consider[key]
                min_time = time_to_pool
        return (closest_pool, min_time)

    def link_to_gmaps(self, start, finish, mode, dep_time=datetime.now()):
        base_url = "https://www.google.com/maps/dir/?api=1&origin={0}&destination={1}&travelmode={2}"
        self.logger.info("Making a link to Gmaps")
        start_str = coord_tuple_to_str(start)
        finish_str = coord_tuple_to_str(finish)
        return base_url.format(start_str, finish_str, mode)

    def link_to_walk(self, finish, start=None):
        if start == None:
            start = self.flat
        return self.link_to_gmaps(start, finish, mode="walking")

    def link_to_transit(self, finish, start=None):
        if start == None:
            start = self.flat
        return self.link_to_gmaps(start, finish, mode="transit")

    def julius_directions(self):
        """ 
        Input:
        - None

        Output:
        - tuple of (int) minutes and link to Gmaps route 
        between the flat and the LSE library

        Uses hardcoded LSE library coordinates.
        """
        lse_library = (51.514659, -0.115751)
        time = self.time_to_transit(lse_library)
        route = self.link_to_transit(lse_library)
        return time, route

    def get_directions(self):
        res = {}
        closest_pool, res["Time_Flat_to_pool"] = self._find_closest_pool()
        res["Route_flat_to_pool"] = self.link_to_walk(closest_pool)
        res["Time_Pool_to_office"] = self.time_to_transit(
            self.office, closest_pool)
        res["Route_pool_to_office"] = self.link_to_transit(
            self.office, closest_pool)
        res["Time_Petr_norm_commute"] = self.time_to_transit(self.office)
        res["Route_norm_commute"] = self.link_to_transit(self.office)
        res["Time_Petr_swim_commute"] = res[
            "Time_Flat_to_pool"] + res["Time_Pool_to_office"]
        res["Time_Julius_to_LSE"], res[
            "Route_Julius_to_LSE"] = self.julius_directions()
        return res


if __name__ == "__main__":
    woodchurch_flat = (51.543258, -0.191341)
    f = DirectionsFromFlat(woodchurch_flat)
    f.get_directions()
