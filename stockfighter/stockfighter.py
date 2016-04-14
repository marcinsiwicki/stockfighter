"""
Module for generic connecting to Stockfighter.io API.
"""

import requests
from functools import partial
from urlparse import urljoin


class Stockfighter(object):
    """
    Class for interfacing with the Stockfighter.io API.
    """

    def __init__(self, api_key, account=None):
        self.api_key = api_key
        self.base_url = 'https://api.stockfighter.io/ob/api/'
        self.account = None

        if account:
            self.account = account

        self._urljoin = partial(urljoin, self.base_url)
        self.session = requests.Session()
        self.session.headers = {'X-Starfighter-Authorization': self.api_key}

    def heartbeat(self):
        """
        Pings Stockfighter.io API to verify it is up.

        :rtype: bool
        """
        url = self._urljoin('heartbeat')
        response = self.session.get(url)
        if response.ok:
            return True
        else:
            raise SystemError("Stockfighter.io API is down!")

    def stocks(self, venue):
        """
        Retrieve the list of stocks available for trading on a venue. Note this
        method only returns the tickers.

        :param: venue, str
        :rtype: list of strings
        """
        url = self._urljoin('venues/{0}/stocks'.format(venue))
        response = self.session.get(url)
        if response.ok:
            return [elem["symbol"] for elem in response.json()["symbols"]]
        else:
            raise KeyError(response.json()["error"])

    def orderbook(self, venue, symbol):
        """
        Returns the order book available for a venue and symbol.
        """
        url = self._urljoin('venues/{0}/stocks/{1}'.format(venue, symbol))
        response = self.session.get(url)
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()["error"])

    def quote(self, venue, symbol):
        """
        Fetches quote for a symbol, venue.

        :param venue: str
        :param symbol: str
        :rtype JSON object representing quote
            https://starfighter.readme.io/docs/a-quote-for-a-stock
        """
        url = self._urljoin('venues/{0}/stocks/{1}/quote'.format(venue,
                                                                 symbol))
        response = self.session.get(url)
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])

    def order(self, venue, symbol, side, quantity, order_type, price=None):
        """
        Sends an order to the selected venue. Converts the price to an int.

        :param venue: str
        :param symbol: str
        :param side: str
        :param price: float
        :param quantity: int
        :param order_type: str
        :rtype JSON order object
            https://starfighter.readme.io/docs/place-new-order
        """
        order = {'venue': venue,
                 'stock': symbol,
                 'qty': quantity,
                 'direction': side,
                 'orderType': order_type,
                 }

        if self.account:
            order['account'] = self.account

        if price:
            order["price"] = int(price * 100)

        url = self._urljoin('venues/{0}/stocks/{1}/orders'.format(venue,
                                                                  symbol))
        response = self.session.post(url, json=order)
        return response.json()

    def order_status(self, venue, symbol, id):
        """
        Check on order status.

        :param id: int
        :rtype JSON order object
        """
        url = self._expand_path(venue, symbol) + '/orders/' + str(id)
        response = self.session.get(url)
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])
