from django.test import TestCase


class SampleTest(TestCase):
    def test_1_equals_1(self):
        self.assertEquals(1, 1)