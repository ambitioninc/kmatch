from copy import deepcopy
from operator import not_, lt, le, eq, ge, ne, gt
import re


class KMatch(object):
    """
    Implements the KMatch language. Takes a dictionary specifying the pattern, compiles it, validates
    it, and provides the user with the match function.
    """
    _OPERATOR_MAP = {
        '&': all,
        '|': any,
        '^': not_,
    }
    _FILTER_MAP = {
        '==': eq,
        '!=': ne,
        '<': lambda value, filter_value: lt(value, filter_value) if value is not None else False,
        '>': lambda value, filter_value: gt(value, filter_value) if value is not None else False,
        '<=': lambda value, filter_value: le(value, filter_value) if value is not None else False,
        '>=': lambda value, filter_value: ge(value, filter_value) if value is not None else False,
        '=~': lambda match_str, regex: regex.match(match_str) if match_str is not None else False,
    }

    def __init__(self, p):
        """
        Sets the pattern, compiles its regexs (if it has any), and performs validation on the pattern.

        :param p: The kmatch pattern
        :type p: dict
        :raises: ValueError on an invalid pattern or regex
        """
        self._pattern = deepcopy(p)

        # Validate the pattern is in the appropriate format
        self._validate(self._pattern)

        # Compile any regexs in the pattern
        self._compile(self._pattern)

    def _is_operator(self, p):
        return len(p) == 2 and p[0] in self._OPERATOR_MAP and isinstance(p[1], (list, tuple))

    def _is_filter(self, p):
        return len(p) == 3 and p[0] in self._FILTER_MAP

    def _compile(self, p):
        """
        Recursively compiles the regexs in the pattern (p).
        """
        if self._is_filter(p):
            if p[0] == '=~':
                try:
                    p[2] = re.compile(p[2])
                except:  # Python doesn't document exactly what exceptions re.compile throws
                    raise ValueError('Bad regex - {0}'.format(p[2]))
        else:
            for operator_or_filter in (p[1] if p[0] != '^' else [p[1]]):
                self._compile(operator_or_filter)

    def _validate(self, p):
        """
        Recursively validates the pattern (p), ensuring it adheres to the proper key names and structure.
        """
        if self._is_operator(p):
            for operator_or_filter in (p[1] if p[0] != '^' else [p[1]]):
                self._validate(operator_or_filter)
        elif not self._is_filter(p):
            raise ValueError('Not a valid operator or filter - {0}'.format(p))

    def _match(self, p, value):
        """
        Calls either _match_operator or _match_operand depending on the pattern (p) provided.
        """
        if self._is_operator(p):
            return self._match_operator(p, value)
        else:
            return self._match_filter(p, value)

    def _match_operator(self, p, value):
        """
        Returns True or False if the operator (&, |, or ^ with filters) matches the value dictionary.
        """
        if p[0] == '^':
            return self._OPERATOR_MAP[p[0]](self._match(p[1], value))
        else:
            return self._OPERATOR_MAP[p[0]]([self._match(operator_or_filter, value) for operator_or_filter in p[1]])

    def _match_filter(self, p, value):
        """
        Returns True of False if value matches the filter.
        """
        return self._FILTER_MAP[p[0]](value.get(p[1]), p[2])

    def match(self, value):
        """
        Matches the value to the pattern

        :param value: The value to be matched
        :type value: dict
        :returns: True if the value matches the pattern, False otherwise
        """
        return self._match(self._pattern, value)
