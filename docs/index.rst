Documentation for Stockfighter Client
=====================================

Stockfighter.io
---------------

`Stockfighter`_ is a programming game provided by the fine folks at `Starfighter`_. They
provide a REST API documented on their site to handle the challenges as well as start
and restart levels. I recommend reading the `docs`_ to get familiar with some of the API
details before using the wrappers in this project.

.. _Stockfighter: https://www.stockfighter.io/
.. _Starfighter: http://www.starfighters.io/
.. _docs: https://starfighter.readme.io/v1.0/docs

Project Info
------------

This project consists of a ``stockfighter`` module that includes clients for
interacting with Stockfighter and Gamemaster APIs. A utility class is
provided for choosing the supported order types.

The ``Stockfighter`` class relies on the REST API to communicate with the exchanges
and venues. Support for the websockets has not yet been integrated.


Release History
---------------

v 0.10 (04/30/2016)
~~~~~~~~~~~~~~~~~~~
Features:

* Gamemaster API client
* Stockfighter API client
* OrderType enum for easier order sending

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Stockfighter Client

   stockfighter_doc

.. toctree::
   :maxdepth: 2
   :caption: Specifying Order Types

   ordertype

.. toctree::
   :maxdepth: 2
   :caption: Interacting with Gamemaster

   gamemaster
