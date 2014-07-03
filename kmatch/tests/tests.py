from unittest import TestCase
from mock import patch

from kmatch import KMatch


class KMatchMatchTest(TestCase):
    """
    Tests the match function in KMatch.
    """
    def test_basic_lte_true(self):
        self.assertTrue(KMatch(['<=', 'f', 0]).match({'f': -1}))

    def test_basic_lte_false(self):
        self.assertFalse(KMatch(['<=', 'f', 0]).match({'f': 1}))

    def test_basic_lte_non_extant(self):
        self.assertFalse(KMatch(['<=', 'f', 0]).match({}))

    def test_basic_lt_non_extant(self):
        self.assertFalse(KMatch(['<', 'f', 0]).match({}))

    def test_basic_eq_true(self):
        self.assertTrue(KMatch(['==', 'f', 0]).match({'f': 0}))

    def test_basic_eq_false(self):
        self.assertFalse(KMatch(['==', 'f', 0]).match({'f': 1}))

    def test_basic_eq_non_extant(self):
        self.assertFalse(KMatch(['==', 'f', 0]).match({}))

    def test_basic_gte_true(self):
        self.assertTrue(KMatch(['>=', 'f', 0]).match({'f': 0}))

    def test_basic_gte_false(self):
        self.assertFalse(KMatch(['>=', 'f', 0]).match({'f': -1}))

    def test_basic_gte_non_extant(self):
        self.assertFalse(KMatch(['>=', 'f', 0]).match({}))

    def test_basic_gt_non_extant(self):
        self.assertFalse(KMatch(['>', 'f', 0]).match({}))

    def test_basic_regex_true(self):
        self.assertTrue(KMatch(['=~', 'f', '^hi$']).match({'f': 'hi'}))

    def test_basic_regex_false(self):
        self.assertFalse(KMatch(['=~', 'f', '^hi$']).match({'f': ' hi'}))

    def test_basic_regex_non_extant(self):
        self.assertFalse(KMatch(['=~', 'f', '^hi$']).match({}))

    def test_basic_no_key_is_none_true(self):
        self.assertTrue(KMatch(['==', 'f', None]).match({}))

    def test_basic_no_key_is_not_none_false(self):
        self.assertFalse(KMatch(['!=', 'f', None]).match({}))

    def test_basic_no_key_regex_false(self):
        self.assertFalse(KMatch(['=~', 'f', 'a']).match({}))

    def test_not_field_true(self):
        self.assertTrue(KMatch([
            '!', ['>=', 'f', 3],
        ]).match({'f': 1}))

    def test_compound_and_lte_gte_single_field_true(self):
        self.assertTrue(KMatch([
            '&', [
                ['>=', 'f', 3],
                ['<=', 'f', 7],
            ]
        ]).match({'f': 5}))

    def test_compound_and_lte_gte_double_field_true(self):
        self.assertTrue(KMatch([
            '&', [
                ['>=', 'f1', 3],
                ['<=', 'f2', 7],
            ]
        ]).match({'f1': 5, 'f2': 0}))

    def test_compound_or_regex_double_field_true(self):
        self.assertTrue(KMatch([
            '|', [
                ['=~', 'f1', '^Email$'],
                ['=~', 'f2', '^Call$'],
            ]
        ]).match({'f1': 'Email', 'f2': 'Reminder'}))

    def test_compound_or_regex_double_field_false(self):
        self.assertFalse(KMatch([
            '|', [
                ['=~', 'f1', '^Email$'],
                ['=~', 'f2', '^Call$'],
            ]
        ]).match({'f1': 'Emails', 'f2': 'Reminder'}))

    def test_nested_compound_or_and_regex_double_field_true(self):
        self.assertTrue(KMatch([
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
        self.assertFalse(KMatch([
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
        self.assertTrue(KMatch([
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
        ]).match({'f1': 'Call', 'f3': 2}))

    def test_two_nested_ors_false(self):
        self.assertFalse(KMatch([
            '&', [
                ['|', [
                    ['=~', 'f1', '^Email$'],
                    ['=~', 'f1', '^Call$'],
                ]],
                ['!', ['>=', 'f2', 3]],
            ]
        ]).match({'f1': 'Call', 'f2': 4}))

    def test_string_choice_or_true(self):
        self.assertTrue(KMatch([
            '|', [
                ['==', 'f1', 'Email'],
                ['==', 'f1', 'Call'],
                ['==', 'f1', 'Task'],
            ]
        ]).match({'f1': 'Task', 'f2': 2}))


class KMatchInitTest(TestCase):
    """
    Tests the init function in KMatch, which validates and compiles the pattern.
    """
    def test_empty(self):
        with self.assertRaises(ValueError):
            KMatch([])

    def test_null_regex(self):
        with self.assertRaises(ValueError):
            KMatch(['=~', 'f', None])

    def test_invalid_regex(self):
        with self.assertRaises(ValueError):
            KMatch(['=~', 'f', []])

    def test_non_list_operand(self):
        with self.assertRaises(ValueError):
            KMatch(['&', {}])

    def test_invalid_operator_name(self):
        with self.assertRaises(ValueError):
            KMatch(['INVALID', ['=~', 'f', 'r']])

    def test_no_field_key_present(self):
        with self.assertRaises(ValueError):
            KMatch(['>=', 'r'])

    def test_invalid_filter_key(self):
        with self.assertRaises(ValueError):
            KMatch(['r', 'invalid_filter', 'r'])

    def test_too_many_filters(self):
        with self.assertRaises(ValueError):
            KMatch(['r', '=~', 'r', '>=', 'r'])

    def test_non_dict_list(self):
        with self.assertRaises(ValueError):
            KMatch('aaa')

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_unnested(self, mock_compile):
        k = KMatch(['=~', 'field', 'hi'])
        self.assertEquals(mock_compile.call_count, 1)
        self.assertEquals(k._pattern, ['=~', 'field', 'hi_compiled'])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_nested_list_of_single_dict(self, mock_compile):
        k = KMatch(['!', ['=~', 'field', 'hi']])
        self.assertEquals(mock_compile.call_count, 1)
        self.assertEquals(k._pattern, ['!', ['=~', 'field', 'hi_compiled']])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_nested_list_of_lists(self, mock_compile):
        k = KMatch(['&', [['=~', 'f', 'hi'], ['=~', 'f', 'hello']]])
        self.assertEquals(mock_compile.call_count, 2)
        self.assertEquals(
            k._pattern,
            ['&', [['=~', 'f', 'hi_compiled'], ['=~', 'f', 'hello_compiled']]])

    @patch('kmatch.kmatch.re.compile', spec_set=True, side_effect=lambda x: '{0}_compiled'.format(x))
    def test_triply_nested_list_of_dicts(self, mock_compile):
        k = KMatch(['&', [
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
        self.assertEquals(k._pattern, ['&', [
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
