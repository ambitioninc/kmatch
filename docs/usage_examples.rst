Usage examples
==============

Here we provide some brief usage examples of the code.

Importing, compiling, and validating a kmatch pattern
-----------------------------------------------------
The KMatch object can be imported directly from kmatch

.. code-block:: python

    from kmatch import KMatch

Once imported, simply instantiating the KMatch object performs validation. It also compiles any regular expressions that are in the pattern for faster ``match`` function calls.

.. code-block:: python

    k = KMatch(['k1', '>', 2])


Performing simple filters
-------------------------
Simple single filters can be used directly when a logical operator is not needed. For example, performing a regex match on a key that has the `@` symbol:

.. code-block:: python

    print KMatch(['k', '=~', '.*@.*']).match({'k': 'person@mail.com'})
    True

This also applies to filtering numerical values:

.. code-block:: python

    print KMatch(['num', '>', 15]).match({'num': 16})
    True

    print KMatch(['num', '<=', 7]).match({'num': 8})
    False


More complex filters
--------------------
Filters can be combined with the ``&`` (``AND``) logical operator for more complex filtering:

.. code-block:: python

    print KMatch(['&', [
        ['k1', '>', 0],
        ['k2', '<=', 5],
    ]]).match({
        'k1': 50,
        'k2': 1,
    })
    True

The same can be done with the ``|`` (``OR``) logical operator:

.. code-block:: python

    print KMatch(['|', [
        ['k1', '==', 'Hello'],
        ['k1', '==', 'World'],
        ['k1', '==', '!'],
    ]]).match({'k1': 'Hi'})
    False

The ``^`` (``NOT``) logical operator operates on a single filter (or logical combination of filters):

.. code-block:: python

    print KMatch(['^', ['k', '==', 0]]).match({'k', 1})
    True

Operators can be combined in various ways to form more complex patterns like so:

.. code-block:: python

    print KMatch(['|', [
        ['&', [
            ['k1', '==', 3],
            ['k2', '==', 4],
        ]],
        ['^', ['val', '=~', '.*Hello.*']],
    ]]).match({
        'k1': 4,
        'k2': 5,
        'val', 'Hi',
    })
    True

A reminder about existence checking
-----------------------------------
Remember that if the keys don't exist, ``None`` is returned as the value in the dictionary. The ``==`` and ``!=`` operators can be used to check for ``None``, however, all other filters will return ``False``. For example:

.. code-block:: python

    print KMatch(['k1', '>', 5]).match({})
    False

    print KMatch('k1', '==', None).match({})
    True

.. note:: We are still figuring out how to integrate existence checking in the language so that users will have more power of checking if a key is actually ``None`` or if it doesn't exist. Do a pull request and help us flesh this out!
