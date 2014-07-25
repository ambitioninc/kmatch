from .kmatch import K


class kmatchMixin(object):
    """
    A mixin for test classes to perform kmatch validation on dictionaries
    """
    def assertMatches(self, pattern, value, suppress_key_errors=False):
        """
        Assert that the value matches the kmatch pattern.

        :type pattern: list
        :param pattern: The kmatch pattern

        :type value: dict
        :param value: The dictionary to evaluate

        :type suppress_key_errors: bool
        :param suppress_key_errors: Suppress KeyError exceptions on filters and return False instead. False by default

        :raises:
            * :class:`KeyError <exceptions.KeyError>` if key from pattern does not exist in input value and the \
            suppress_key_errors class variable is False
            * :class:`AssertionError <exceptions.AssertionError>` if the value **does not** match the pattern
        """
        assert K(pattern, suppress_key_errors=suppress_key_errors).match(value)

    def assertNotMatches(self, pattern, value, suppress_key_errors=True):
        """
        Assert that the value does **not** matches the kmatch pattern.

        :type pattern: list
        :param pattern: The kmatch pattern

        :type value: dict
        :param value: The dictionary to evaluate

        :type suppress_key_errors: bool
        :param suppress_key_errors: Suppress KeyError exceptions on filters and return False instead. True by default

        :raises:
            * :class:`KeyError <exceptions.KeyError>` if key from pattern does not exist in input value and the \
            suppress_key_errors class variable is False
            * :class:`AssertionError <exceptions.AssertionError>` if the value **does match** the pattern
        """
        assert not K(pattern, suppress_key_errors=suppress_key_errors).match(value)
