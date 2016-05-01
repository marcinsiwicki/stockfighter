Stockfighter
============

Suggestions
***********

Documentation of JSON responses can be found in the linked Stockfighter docs.

If participating in a level with a single venue and symbol, it may be beneficial
to use ``functools`` to simplify the order placement, status checking, and other functions.

.. code-block:: python

   sf = Stockfighter(API_KEY, 'TEST_ACCT')
   order = functools.partial(sf.order, 'VENUE', 'SYMBOL')

Docs
****

.. autoclass:: stockfighter.Stockfighter
   :members:
