from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from mtgdeck.encoder import (MtgDeckEncodeError,
                             MtgDeckEncoder)


class TestMtgDeckEncodeError(TestCase):
    def test___str__(self):
        try:
            raise MtgDeckEncodeError('a')
        except MtgDeckEncodeError as e:
            self.assertEqual("Could not determine encoding format: ('a',)",
                             str(e))


class TestMtgDeckEncoder(TestCase):
    @patch.multiple(MtgDeckEncoder, __abstractmethods__=set())
    def setUp(self):
        self.encoder = MtgDeckEncoder()

    def test_MtgDeckEncoder(self):
        self.assertRaises(TypeError, MtgDeckEncoder)

    def test__scatter(self):
        obj = {'section': {'card': {'setid': 1}}}
        expected = [('section', 'card', 'setid', 1)]
        actual = list(self.encoder._scatter(obj))
        self.assertListEqual(expected, actual)

    def test_dump(self):
        obj = {}
        fp = StringIO()
        expected = ''
        self.encoder.dump(obj, fp)
        actual = fp.read()
        self.assertEqual(expected, actual)

    def test_dumps(self):
        obj = {}
        expected = ''
        actual = self.encoder.dumps(obj)
        self.assertEqual(expected, actual)
