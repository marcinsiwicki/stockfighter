Stockfighter.io Python Client
===============================

A simple interface for interacting with the Stockfighter and Gamemaster APIs for the
programming challenges at `Stockfighter.io`_.

Included is a utility enum for easier submission of order types (read: avoid typos).

.. code-block:: python

    from stockfighter import Stockfighter, Gamemaster, OrderType
    gm = Gamemaster(SECRET_KEY)
    sf = Stockfighter(SECRET_KEY)

    print sf.heartbeat()

Documentation
-------------

Documentation for this project can be found at `Read the Docs`_.


.. _Stockfighter.io: http://www.stockfighter.io
.. _Read the Docs: http://pystockfighter.rtfd.io/

