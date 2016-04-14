"""
Module for generic connecting to Stockfighter.io API.
"""

import requests
import sys
import json
import pprint


class Stockfighter(object):
    """
    Class for interfacing with the Stockfighter.io API.
    """

    def __init__(self, account=None, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.stockfighter.io/ob/api'
        self.account = None

        if account:
            self.account = account

        self.session = requests.Session()
        self.session.headers = {'X-Starfighter-Authorization': self.api_key}

    def _expand_path(self, venue, symbol):
        """
        Expands self.base_url to include venue and symbol.
        """
        return self.base_url + '/venues/' + venue + '/stocks/' + symbol

    def quote(self, venue, symbol):
        """
        Fetches quote for a symbol, venue.

        :type venue: str
        :type symbol: str
        :rtype JSON object representing quote
            https://starfighter.readme.io/docs/a-quote-for-a-stock
        """
        path = self._expand_path(venue, symbol) + '/quote'
        response = self.session.get(path)
        if response.json()['ok']:
            return response.json()
        else:
            raise KeyError(response.json()['error'])

    def order(self, venue, symbol, side, quantity, order_type, price=None):
        """
        Sends an order to the selected venue. Converts the price to an int.

        :type venue: str
        :type symbol: str
        :type side: str
        :type price: float
        :type quantity: int
        :type order_type: str
        :rtype JSON order object
            https://starfighter.readme.io/docs/place-new-order
        """
        order = {'account': self.account,
                 'venue': venue,
                 'stock': symbol,
                 'qty': quantity,
                 'direction': side,
                 'orderType': order_type,
                 }

        if price:
            order["price"] = int(price * 100)

        path = self._expand_path(venue, symbol) + '/orders'
        response = self.session.post(path, json=order)
        return response.json()

    def order_status(self, venue, symbol, id):
        """
        Check on order status.

        :type id: int
        :rtype JSON order object
        """
        path = self._expand_path(venue, symbol) + '/orders/' + str(id)
        response = self.session.get(path)
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])
