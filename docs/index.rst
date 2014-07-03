kmatch: A language for matching Python dictionaries
===================================================
The kmatch library provides a language for matching Python dictionaries. Patterns are specified as lists of filters combined with logical operators.

A quick example of kmatch is below.

.. code-block:: python

    from kmatch import K

    k = K(['>=', 'k', 10])
    print k.match({'k': 9})
    False

    print k.match({'k': 10})
    True

More powerful expressions can be made to match more types of patterns.

.. code-block:: python

    from kmatch import K

    k = K(['&',
        ['=~', 'k1', '.*Hello.*'],
        ['!=', 'k2', False]
    ])

    # Match all a dictionary whose 'k1' key has a pattern of '.*Hello.*' and whose 'k2' key is not False
    k.match(...)


The kmatch app can be used for a wide variety of applications. One example is filtering a list of dictionaries that match a pattern. Another example is to validate dictionaries passed to a function.

Installation, overview of the language, usage examples, and code documentation are overviewed in the following.
