from unittest import TestCase

from mtgdeck.__init__ import (dumps, loads)


class TestInit(TestCase):
    def test_loads(self):
        string = '1 mname\n'
        expected = [('mname', {'count': 1})]
        actual = loads(string)
        self.assertListEqual(expected, actual)

    def test_dumps(self):
        obj = [('mname', {'count': 1})]
        expected = '1 mname\n'
        actual = dumps(obj)
        self.assertEqual(expected, actual)
