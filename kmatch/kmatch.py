from copy import deepcopy
from operator import not_, lt, le, eq, ge, ne, gt, xor
import re


class K(object):
    """
    Implements the kmatch language. Takes a dictionary specifying the pattern, compiles it, validates
    it, and provides the user with the match function.
    """
    _OPERATOR_MAP = {
        '&': all,
        '|': any,
        '!': not_,
        '^': xor,
    }
    _VALUE_FILTER_MAP = {
        '==': eq,
        '!=': ne,
        '<': lt,
        '>': gt,
        '<=': le,
        '>=': ge,
        '=~': lambda match_str, regex: regex.match(match_str) if match_str is not None else False,
    }
    _KEY_FILTER_MAP = {
        '?': lambda key, value: key in value,
        '!?': lambda key, value: key not in value,
    }

    def __init__(self, p, suppress_key_errors=False):
        """
        Sets the pattern, performs validation on the pattern, and compiles its regexs if it has any.

        :param p: The kmatch pattern
        :type p: list
        :param suppress_key_errors: Suppress KeyError exceptions on filters and return False instead
        :type suppress_key_errors: bool
        :raises: :class:`ValueError <exceptions.ValueError>` on an invalid pattern or regex
        """
        self._raw_pattern = deepcopy(p)
        self._compiled_pattern = deepcopy(p)
        self._suppress_key_errors = suppress_key_errors

        # Validate the pattern is in the appropriate format
        self._validate(self._compiled_pattern)

        # Compile any regexs in the pattern
        self._compile(self._compiled_pattern)

    @property
    def pattern(self):
        """
        Gets the kmatch pattern.

        :returns: The kmatch pattern dictionary originally provided to the K object
        :rtype: list
        """
        return self._raw_pattern

    def _is_operator(self, p):
        return len(p) == 2 and p[0] in self._OPERATOR_MAP and isinstance(p[1], (list, tuple))

    def _is_value_filter(self, p):
        return len(p) == 3 and p[0] in self._VALUE_FILTER_MAP

    def _is_key_filter(self, p):
        return len(p) == 2 and p[0] in self._KEY_FILTER_MAP

    def _compile(self, p):
        """
        Recursively compiles the regexs in the pattern (p).
        """
        if self._is_value_filter(p) and p[0] == '=~':
            try:
                p[2] = re.compile(p[2])
            except:  # Python doesn't document exactly what exceptions re.compile throws
                raise ValueError('Bad regex - {0}'.format(p[2]))
        elif self._is_operator(p):
            for operator_or_filter in (p[1] if p[0] != '!' else [p[1]]):
                self._compile(operator_or_filter)

    def _validate(self, p):
        """
        Recursively validates the pattern (p), ensuring it adheres to the proper key names and structure.
        """
        if self._is_operator(p):
            for operator_or_filter in (p[1] if p[0] != '!' else [p[1]]):
                if p[0] == '^':
                    self._validate_xor_args(p)
                self._validate(operator_or_filter)
        elif not self._is_value_filter(p) and not self._is_key_filter(p):
            raise ValueError('Not a valid operator or filter - {0}'.format(p))

    def _validate_xor_args(self, p):
        """
        Raises ValueError if 2 arguments are not passed to an XOR
        """
        if len(p[1]) != 2:
            raise ValueError('Invalid syntax: XOR only accepts 2 arguments, got {0}: {1}'.format(len(p[1]), p))

    def _match(self, p, value):
        """
        Calls either _match_operator or _match_operand depending on the pattern (p) provided.
        """
        if self._is_operator(p):
            return self._match_operator(p, value)
        else:
            try:
                if self._is_value_filter(p):
                    return self._match_value_filter(p, value)
                else:
                    return self._match_key_filter(p, value)
            except KeyError:
                if self._suppress_key_errors:
                    return False
                else:
                    raise

    def _match_operator(self, p, value):
        """
        Returns True or False if the operator (&, |, or ! with filters, or ^ with filters) matches the value dictionary
        """
        if p[0] == '!':
            return self._OPERATOR_MAP[p[0]](self._match(p[1], value))
        elif p[0] == '^':
            return self._OPERATOR_MAP[p[0]](self._match(p[1][0], value), self._match(p[1][1], value))
        else:
            return self._OPERATOR_MAP[p[0]]([self._match(operator_or_filter, value) for operator_or_filter in p[1]])

    def _match_value_filter(self, p, value):
        """
        Returns True of False if value in the pattern p matches the filter.
        """
        return self._VALUE_FILTER_MAP[p[0]](value[p[1]], p[2])

    def _match_key_filter(self, p, value):
        """
        Returns True of False if key in the pattern p and the value matches the filter.
        """
        return self._KEY_FILTER_MAP[p[0]](p[1], value)

    def match(self, value):
        """
        Matches the value to the pattern.

        :param value: The value to be matched
        :type value: dict
        :rtype: bool
        :returns: True if the value matches the pattern, False otherwise
        :raises: :class:`KeyError <exceptions.KeyError>` if key from pattern does not exist in input value and the
                suppress_key_errors class variable is False
        """
        return self._match(self._compiled_pattern, value)

    def get_field_keys(self, pattern=None):
        """
        Builds a set of all field keys used in the pattern including nested fields.

        :param pattern: The kmatch pattern to get field keys from or None to use self.pattern
        :type pattern: list or None
        :returns: A set object of all field keys used in the pattern
        :rtype: set
        """
        # Use own pattern or passed in argument for recursion
        pattern = pattern or self.pattern
        keys = set()

        # Valid pattern length can only be 2 or 3
        if len(pattern) == 2:
            if pattern[0] in ('&', '|', '^'):
                # Pass each nested pattern to get_field_keys
                for filter_item in pattern[1]:
                    keys = keys.union(self.get_field_keys(filter_item))
            else:
                # pattern[0] == '!'
                keys = keys.union(self.get_field_keys(pattern[1]))
        else:
            # Pattern length is 3
            keys.add(pattern[1])
        return keys
