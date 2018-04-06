from sys import version
from unittest import TestCase
from mock import patch

from kmatch import K


class KPatternTest(TestCase):
    """
    Tests the pattern function in K.
    """
    def test_pattern(self):
        k = K(['=~', 'hi', 'hi'])
        self.assertEquals(k.pattern, ['=~', 'hi', 'hi'])


class KMatchTest(TestCase):
    """
    Tests the match function in K.
    """
    def test_basic_lte_true(self):
        self.assertTrue(K(['<=', 'f', 0]).match({'f': -1}))

    def test_basic_lte_false(self):
        self.assertFalse(K(['<=', 'f', 0]).match({'f': 1}))

    def test_basic_lte_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['<=', 'f', 0]).match({}))

    def test_basic_lt_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['<', 'f', 0]).match({}))

    def test_basic_eq_true(self):
        self.assertTrue(K(['==', 'f', 0]).match({'f': 0}))

    def test_basic_eq_false(self):
        self.assertFalse(K(['==', 'f', 0]).match({'f': 1}))

    def test_basic_eq_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['==', 'f', 0]).match({}))

    def test_basic_gte_true(self):
        self.assertTrue(K(['>=', 'f', 0]).match({'f': 0}))

    def test_basic_gte_false(self):
        self.assertFalse(K(['>=', 'f', 0]).match({'f': -1}))

    def test_basic_gte_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['>=', 'f', 0]).match({}))

    def test_basic_gt_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['>', 'f', 0]).match({}))

    def test_null_regex_match_false(self):
        self.assertFalse(K(['=~', 'f', '^hi$']).match({'f': None}))

    def test_basic_regex_true(self):
        self.assertTrue(K(['=~', 'f', '^hi$']).match({'f': 'hi'}))

    def test_basic_regex_false(self):
        self.assertFalse(K(['=~', 'f', '^hi$']).match({'f': ' hi'}))

    def test_basic_regex_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['=~', 'f', '^hi$']).match({}))

    def test_basic_equals_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertTrue(K(['==', 'f', None]).match({}))

    def test_basic_not_equals_non_extant(self):
        with self.assertRaises(KeyError):
            self.assertFalse(K(['!=', 'f', None]).match({}))

    def test_basic_existence_true(self):
        self.assertTrue(K(['?', 'k']).match({'k': 'val'}))

    def test_basic_existence_false(self):
        self.assertFalse(K(['?', 'k']).match({'k1': 'val'}))

    def test_basic_nonexistence_true(self):
        self.assertTrue(K(['!?', 'k']).match({'k1': 'val'}))

    def test_basic_nonexistence_false(self):
        self.assertFalse(K(['!?', 'k']).match({'k': 'val'}))

    def test_basic_suppress_key_errors(self):
        self.assertFalse(K(['==', 'k', 3], suppress_key_errors=True).match({}))

    def test_basic_suppress_exceptions(self):
        self.assertFalse(K(['==', 'k', 3], suppress_exceptions=True).match({}))

    def test_not_field_true(self):
        self.assertTrue(K([
            '!', ['>=', 'f', 3],
        ]).match({'f': 1}))

    def test_compound_suppress_key_errors_gte_true(self):
        self.assertTrue(K([
            '|', [
                ['==', 'f1', 5],
                ['>', 'f', 5],
            ]
        ], suppress_key_errors=True).match({'f': 6}))

    def test_compound_suppress_exceptions_gte_true(self):
        self.assertTrue(K([
            '|', [
                ['==', 'f1', 5],
                ['>', 'f', 5],
            ]
        ], suppress_exceptions=True).match({'f': 6}))

    def test_type_exception(self):
        """
        Handles different data type comparisons in py3
        """
        if version[0] == '2':  # pragma: no cover
            with patch('kmatch.K._match_value_filter') as mock_match_value_filter:
                mock_match_value_filter.side_effect = TypeError

                with self.assertRaises(TypeError):
                    K(['>=', 'k', 3]).match({'k': None})
                with self.assertRaises(TypeError):
                    K(['>=', 'k', 3]).match({'k': ''})
                self.assertFalse(K(['>=', 'k', 3], suppress_exceptions=True).match({'k': None}))
                self.assertFalse(K(['>=', 'k', 3], suppress_exceptions=True).match({'k': ''}))

        if version[0] == '3':  # pragma: no cover
            with self.assertRaises(TypeError):
                K(['>=', 'k', 3]).match({'k': None})
            with self.assertRaises(TypeError):
                K(['>=', 'k', 3]).match({'k': ''})
            self.assertFalse(K(['>=', 'k', 3], suppress_exceptions=True).match({'k': None}))
            self.assertFalse(K(['>=', 'k', 3], suppress_exceptions=True).match({'k': ''}))

    def test_compound_existence_gte_true(self):
        self.assertTrue(K([
            '&', [
                ['?', 'f'],
                ['>', 'f', 5],
            ]
        ]).match({'f': 6}))

    def test_compound_and_lte_gte_single_field_true(self):
        self.assertTrue(K([
            '&', [
                ['>=', 'f', 3],
                ['<=', 'f', 7],
            ]
        ]).match({'f': 5}))

    def test_compound_and_lte_gte_double_field_true(self):
        self.assertTrue(K([
            '&', [
                ['>=', 'f1', 3],
                ['<=', 'f2', 7],
            ]
        ]).match({'f1': 5, 'f2': 0}))

    def test_compound_or_regex_double_field_true(self):
        self.assertTrue(K([
            '|', [
                ['=~', 'f1', '^Email$'],
                ['=~', 'f2', '^Call$'],
            ]
        ]).match({'f1': 'Email', 'f2': 'Reminder'}))

    def test_compound_or_regex_double_field_false(self):
        self.assertFalse(K([
            '|', [
                ['=~', 'f1', '^Email$'],
                ['=~', 'f2', '^Call$'],
            ]
        ]).match({'f1': 'Emails', 'f2': 'Reminder'}))

    def test_nested_compound_or_and_regex_double_field_true(self):
        self.assertTrue(K([
            '&', [
                ['>=', 'f2', 10], [
                    '|', [
                        ['=~', 'f1', '^Email$'],
                        ['=~', 'f1', '^Call$'],
                    ]
                ]
            ]
        ]).match({'f1': 'Email', 'f2': 20}))

    def test_nested_compound_or_and_regex_double_field_false(self):
        self.assertFalse(K([
            '&', [
                ['>=', 'f2', 10], [
                    '|', [
                        ['=~', 'f1', '^Email$'],
                        ['=~', 'f1', '^Call$'],
                    ]
                ]
            ]
        ]).match({'f1': 'Email', 'f2': 2}))

    def test_two_nested_ors_true(self):
        self.assertTrue(K([
            '&', [
                ['|', [
                    ['=~', 'f1', '^Email$'],
                    ['=~', 'f1', '^Call$'],
                ]],
                ['|', [
                    ['>=', 'f2', 3],
                    ['>=', 'f3', 1],
                ]]
            ]
        ]).match({'f1': 'Call', 'f2': 5, 'f3': 2}))

    def test_two_nested_ors_false(self):
        self.assertFalse(K([
            '&', [
                ['|', [
                    ['=~', 'f1', '^Email$'],
                    ['=~', 'f1', '^Call$'],
                ]],
                ['!', ['>=', 'f2', 3]],
            ]
        ]).match({'f1': 'Call', 'f2': 4}))

    def test_string_choice_or_true(self):
        self.assertTrue(K([
            '|', [
                ['==', 'f1', 'Email'],
                ['==', 'f1', 'Call'],
                ['==', 'f1', 'Task'],
            ]
        ]).match({'f1': 'Task', 'f2': 2}))

    def test_xor_true(self):
        self.assertTrue(K([
            '^', [
                ['?', 'email'],
                ['?', 'e-mail']
            ]
        ]).match({'email': 'opensource@ambition.com'}))
        self.assertTrue(K([
            '^', [
                ['?', 'email'],
                ['?', 'e-mail']
            ]
        ]).match({'e-mail': 'opensource@ambition.com'}))

    def test_xor_false(self):
        self.assertFalse(K([
            '^', [
                ['?', 'email'],
                ['?', 'e-mail']
            ]
        ]).match({'email': 'opensource@ambition.com',
                  'e-mail': 'opensource@ambition.com'}))

    def test_get_field_keys(self):
        """
        Verifies that all field keys are returned
        """
        pattern = ['&', [
            ['?', 'foo'],
            ['=~', 'one', 'one value'],
            ['=~', 'two', 'two value'],
            ['|', [
                ['=~', 'three', 'three value'],
                ['!', ['=~', 'one', 'other one value']],
                ['^', [
                    ['==', 'five', 'five value'],
                    ['==', 'five', 'five value']
                ]],
                ['&', [
                    ['=~', 'four', 'four value'],
                ]]
            ]],
        ]]
        self.assertEqual(K(pattern).get_field_keys(), set(['one', 'two', 'three', 'four', 'five', 'foo']))

    def test_get_field_keys_invalid_pattern(self):
        """
        Verifies that an error is raised for invalid patterns
        """
        pattern = ['&', [
            ['invalid', 'one', 'one value']
        ]]
        with self.assertRaises(ValueError):
            K(pattern).get_field_keys()

    def test_properties(self):
        k = K(['<=', 'f', 0])
        self.assertFalse(k.suppress_exceptions)
        k.suppress_exceptions = True
        self.assertTrue(k.suppress_exceptions)


class KInitTest(TestCase):
    """
    Tests the init function in K, which validates and compiles the pattern.
    """
    def test_empty(self):
        with self.assertRaises(ValueError):
            K([])

    def test_null_regex(self):
        with self.assertRaises(ValueError):
            K(['=~', 'f', None])

    def test_invalid_regex(self):
        with self.assertRaises(ValueError):
            K(['=~', 'f', []])

    def test_non_list_operand(self):
        with self.assertRaises(ValueError):
            K(['&', {}])

    def test_invalid_operator_name(self):
        with self.assertRaises(ValueError):
            K(['INVALID', ['=~', 'f', 'r']])

    def test_no_field_key_present(self):
        with self.assertRaises(ValueError):
            K(['>=', 'r'])

    def test_invalid_filter_key(self):
        with self.assertRaises(ValueError):
            K(['r', 'invalid_filter', 'r'])

    def test_too_many_filters(self):
        with self.assertRaises(ValueError):
            K(['r', '=~', 'r', '>=', 'r'])

    def test_non_dict_list(self):
        with self.assertRaises(ValueError):
            K('aaa')

    def test_invalid_xor(self):
        with self.assertRaises(ValueError):
            K([
                '^',
                [
                    ['?', 'a'],
                    ['?', 'b'],
                    ['?', 'c']
                ]
            ])
        with self.assertRaises(ValueError):
            K([
                '^',
                [
                    ['?', 'a'],
                ]
            ])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_unnested(self, mock_compile):
        k = K(['=~', 'field', 'hi'])
        self.assertEquals(mock_compile.call_count, 1)
        self.assertEquals(k._compiled_pattern, ['=~', 'field', 'hi_compiled'])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_nested_list_of_single_dict(self, mock_compile):
        k = K(['!', ['=~', 'field', 'hi']])
        self.assertEquals(mock_compile.call_count, 1)
        self.assertEquals(k._compiled_pattern, ['!', ['=~', 'field', 'hi_compiled']])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_nested_list_of_lists(self, mock_compile):
        k = K(['&', [['=~', 'f', 'hi'], ['=~', 'f', 'hello']]])
        self.assertEquals(mock_compile.call_count, 2)
        self.assertEquals(
            k._compiled_pattern,
            ['&', [['=~', 'f', 'hi_compiled'], ['=~', 'f', 'hello_compiled']]])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_triply_nested_list_of_dicts(self, mock_compile):
        k = K(['&', [
            ['=~', 'f', 'hi'],
            ['=~', 'f', 'hello'],
            ['|', [
                ['=~', 'f', 'or_hi'],
                ['=~', 'f', 'or_hello'],
                ['&', [
                    ['=~', 'f', 'and_hi'],
                ]]
            ]]
        ]])
        self.assertEquals(mock_compile.call_count, 5)
        self.assertEquals(k._compiled_pattern, ['&', [
            ['=~', 'f', 'hi_compiled'],
            ['=~', 'f', 'hello_compiled'],
            ['|', [
                ['=~', 'f', 'or_hi_compiled'],
                ['=~', 'f', 'or_hello_compiled'],
                ['&', [
                    ['=~', 'f', 'and_hi_compiled'],
                ]]
            ]]
        ]])
