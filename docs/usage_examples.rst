Usage examples
==============

Here we provide some brief usage examples of the code.

Importing, compiling, and validating a kmatch pattern
-----------------------------------------------------
The K object can be imported directly from kmatch

.. code-block:: python

    from kmatch import K

Once imported, simply instantiating the K object performs validation on the pattern. It also compiles any regular expressions that are in the pattern for faster ``match`` function calls.

.. code-block:: python

    k = K(['>', 'k1', 2])


Performing simple value filters
-------------------------------
Simple value filters can be used directly when a logical operator is not needed. For example, performing a regex match on a key that has the '@' symbol:

.. code-block:: python

    print K(['=~', 'k', '.*@.*']).match({'k': 'person@mail.com'})
    True

This also applies to filtering numerical values:

.. code-block:: python

    print K(['>', 'num', 15]).match({'num': 16})
    True

    print K(['<=', 'num', 7]).match({'num': 8})
    False


Performing simple key filters
-----------------------------
Simple key filters can also be done to match dictionaries that have a key named 'k1':

.. code-block:: python

    print K(['?', 'k1']).match({'k1': True})
    True

The inverse can also be checked:

.. code-block:: python

    print K(['!?', 'k1']).match({'k2': 'value'})
    True

In the above example, 'k1' does not exist in the matched dictionary, so ``True`` is returned.


Performing logical operations across filters
--------------------------------------------
Filters can be combined with the ``&`` (``AND``) logical operator for more complex filtering:

.. code-block:: python

    print K(['&', [
        ['>', 'k1', 0],
        ['<=', 'k2', 5],
    ]]).match({
        'k1': 50,
        'k2': 1,
    })
    True

The same can be done with the ``|`` (``OR``) logical operator:

.. code-block:: python

    print K(['|', [
        ['==', 'k1', 'Hello'],
        ['==', 'k1', 'World'],
        ['==', 'k1', '!'],
    ]]).match({'k1': 'Hi'})
    False

The ``!`` (``NOT``) logical operator operates on a single filter (or logical combination of filters):

.. code-block:: python

    print K(['!', ['==', 'k', 0]]).match({'k', 1})
    True

Operators can be combined in various ways to form more complex patterns like so:

.. code-block:: python

    print K(['|', [
        ['&', [
            ['==', 'k1', 3],
            ['==', 'k2', 4],
        ]],
        ['!', ['=~', 'val', '.*Hello.*']],
    ]]).match({
        'k1': 4,
        'k2': 5,
        'val', 'Hi',
    })
    True

Filtering with non-extant keys and suppressing KeyErrors
--------------------------------------------------------
If keys from a kmatch pattern do not exist in the matched dictionary, the default behavior is to throw a ``KeyError`` exception:

.. code-block:: python

    K(['==', 'k1', 5]).match({'k2': 1})
    Traceback (most recent call last):
        # Traceback message here ...
    KeyError: 'k1'

This behavior, however, is not always desirable when matching dictionaries that have many keys that may or may not exist. It can be cumbersome to always have to check for existence along with doing filtering. To avoid this scenario, the ``K`` object comes with an optional ``suppress_key_errors`` flag that defaults to ``False``. If set to ``True``, the value ``False`` will be returned any time a key does not exist for an associated filter instead of a ``KeyError`` being raised.

Take our previous example, except with ``suppress_key_errors`` set to ``True``.

.. code-block:: python
    
    print K(['==', 'k1', 5], suppress_key_errors=True).match({'k2': 1})
    False

Using the test mixin
--------------------

The ``kmatchMixin`` can be used for test classes when you want to verify a dictionary matches a particular pattern.

 .. code-block:: python

    from unittest import TestCase
    from kmatch import kmatchMixin


    class MyTestClass(kmatchMixin, TestCase):
        def my_test(self):
            self.assertMatches(['<=', 'f', 0], {'f': -1})

        def my_opposite_test(self):
            with self.assertRaises(AssertionError):
                self.assertNotMatches(['<=', 'f', 0], {'f': -1})

            self.assertNotMatches(['<=', 'f', 0], {'g': 1})


.. note:: The ``suppress_key_errors`` parameter is set to ``False`` by default for ``.assertMatches()``, and ``True``
    for ``.assertNotMatches()``.
