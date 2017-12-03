from unittest import TestCase
from unittest.mock import patch

from mtgdeck.encoder import MtgDeckEncoder


class TestMtgDeckDecoder(TestCase):
    def test_noinstantiation(self):
        self.assertRaises(TypeError, MtgDeckEncoder)

    @patch.multiple(MtgDeckEncoder, __abstractmethods__=set())
    def test__gather(self):
        obj = {'section': {'card': {'setid': 0}}}
        expected = [('section', 'card', 'setid', 0)]
        actual = list(MtgDeckEncoder()._scatter(obj))
        self.assertListEqual(expected, actual)
