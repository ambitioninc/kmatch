Language overview
=================
K provides a language built around filters that are specified in prefix notation as an array or tuple with 3 values. The filters are then combined by operators in prefix notation.

The first value is the filter operator. The second value is the key in the dictionary being matched. The final value is the comparison value. A filter for when 'value' is greater than '3' looks like this:

.. code-block:: python

    ['>', 'value', 3]

The following are all valid operators:

    * ``>`` Performs a greater than filter
    * ``>=`` Performs a greater than or equal to filter
    * ``<`` Performs a less than filter
    * ``<=`` Performs a less than or equal to filter
    * ``==`` Performs an equal to filter
    * ``!=`` Performs a not equal to filter
    * ``=~`` Performs a regex match filter

.. note:: There is currently no support for an existence operator. If the key in the dictionary does not exist, the ``==`` and ``!=`` operators will use ``None`` as the key's value. All of the other operators will return ``False``.

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
    ]]

The above matches dictionaries that have keys 'k1' and 'k2' greater than 4 or keys 'k3' and 'k4' less than 5.