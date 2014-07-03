Language overview
=================
The kmatch library provides a language built around filters that are specified in prefix notation. Filters can operate directly on keys or on the values of the keys in the dictionary passed to the ``match`` function. Filters can be combined together by logical operators in prefix notation.


Value filters
-------------
The values referenced by keys in the kmatch pattern can be filtered by using an operator, the key name, and the comparison value. For example:

.. code-block:: python

    ['>', 'key_name', 3]

The above will return ``True`` when the value of ``key_name`` is greater than 3.

The following are all valid value filter operators:

    * ``>`` Performs a greater than filter
    * ``>=`` Performs a greater than or equal to filter
    * ``<`` Performs a less than filter
    * ``<=`` Performs a less than or equal to filter
    * ``==`` Performs an equal to filter
    * ``!=`` Performs a not equal to filter
    * ``=~`` Performs a regex match filter

Key filters
-----------
Along with filtering on values referenced by keys, the keys themselves can be filtered by using an operator and the key name. For example:

.. code-block:: python

    ['?', 'key_name']

The following are all valid key filter operators:

    * ``?`` Performs an existence filter
    * ``!?`` Performs a non-existence filter

Logical operations across filters
---------------------------------

Filters can then be joined together with the following logical operators in prefix notation:

    * ``&`` Performs a logical ``AND`` on a list of filters
    * ``|`` Performs a logical ``OR`` on a list of filters
    * ``!`` Performs a logical ``NOT`` on a single filter

The notation for ``AND`` looks like the following:

.. code-block:: python

    ['&', [
        ['<', 'k1', 5],
        ['==', 'k2', True],
    ]]

The notation for ``OR`` is similar to ``AND``. The ``NOT`` operator works on a single filter like so:

.. code-block:: python

    ['!', ['=~', 'k1', '^Email$']]

Expressions can be combined as needed to do more complex matching:

.. code-block:: python

    ['|', [
        ['&', [
            ['>', 'k1', 4],
            ['>', 'k2', 4],
        ]],
        ['&', [
            ['<', 'k3', 5],
            ['<', 'k4', 5],
        ]],
        ['!?', 'k5']
    ]]

The above matches dictionaries that have keys 'k1' and 'k2' greater than 4 or keys 'k3' and 'k4' less than 5 or no keys named 'k5'.