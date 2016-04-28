"""
Module for generic connecting to Stockfighter.io API.
"""

import requests
from functools import partial
from enum import Enum
from urlparse import urljoin


class OrderType(Enum):
    market = 1
    limit = 2
    fok = 3
    ioc = 4

    def __str__(self):
        """
        Convert enums to Stockfighter.io accepted strings.
        """
        conversions = {1: 'market',
                       2: 'limit',
                       3: 'fill-or-kill',
                       4: 'immediate-or-cancel'}
        return conversions[self.value]


class Stockfighter(object):
    """
    Class for interfacing with the Stockfighter.io API.

    :param api_key: string containing private key
    :param account: optional account string
    """

    def __init__(self, api_key, account=None):
        self.api_key = api_key
        self.base_url = 'https://api.stockfighter.io/ob/api/'
        self.account = None

        if account:
            self.account = account

        self._urljoin = partial(urljoin, self.base_url)
        self.session = requests.Session()
        headers = {'X-Starfighter-Authorization': self.api_key}
        self.session.headers.update(headers)

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
            raise SystemError('Stockfighter.io API is down!')

    def venue_heartbeat(self, venue):
        """
        Pings a venue to verify it is up.

        :rtype: bool
        """
        url = 'venues/{0}/heartbeat'.format(venue)
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return True
        else:
            raise SystemError('Venue {0} not up!'.format(venue))

    def stocks(self, venue):
        """
        Retrieve the list of stocks available for trading on a venue. Note this
        method only returns the tickers.

        :param: venue, str
        :rtype: list of strings
        """
        url = 'venues/{0}/stocks'.format(venue)
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return [elem['symbol'] for elem in response.json()['symbols']]
        else:
            raise KeyError(response.json()['error'])

    def orderbook(self, venue, symbol):
        """
        Returns the order book available for a venue and symbol.
        """
        url = 'venues/{0}/stocks/{1}'.format(venue, symbol)
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])

    def quote(self, venue, symbol):
        """
        Fetches quote for a symbol, venue.

        :param venue: str
        :param symbol: str
        :rtype JSON object representing quote
            https://starfighter.readme.io/docs/a-quote-for-a-stock
        """
        url = 'venues/{0}/stocks/{1}/quote'.format(venue, symbol)
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])

    def order(self, venue, symbol, side, quantity, ordertype, price=None):
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
        if side not in ('buy', 'sell'):
            raise KeyError('Wrong order type passed, not buy or sell')

        order = {'venue': venue,
                 'stock': symbol,
                 'qty': quantity,
                 'direction': side,
                 'orderType': str(ordertype),
                 }

        if self.account:
            order['account'] = self.account

        # will throw KeyError if no price provided for non market
        if ordertype != OrderType.market:
            order["price"] = price

        url = 'venues/{0}/stocks/{1}/orders'.format(venue, symbol)
        response = self.session.post(self._urljoin(url), json=order)
        return response.json()

    def order_status(self, venue, symbol, orderId):
        """
        Check on order status.

        :param id: int
        :rtype JSON order object
        """
        url = 'venues/{0}/stocks/{1}/orders/{2}'.format(venue, symbol, orderId)
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])

    def cancel_order(self, venue, symbol, orderId):
        """
        Cancels a given order.
        """
        url = 'venues/{0}/stocks/{1}/orders/{2}/cancel'.format(venue, symbol, orderId)
        response = self.session.post(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError(response.json()['error'])

