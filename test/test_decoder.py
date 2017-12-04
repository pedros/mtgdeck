from unittest import TestCase
from unittest.mock import patch

from io import StringIO
from mtgdeck.decoder import (MtgDeckDecodeError,
                             MtgDeckDecoder,
                             MtgDeckAutoDecoder,
                             MtgDeckMagicWorkstationDecoder,
                             MtgDeckOCTGNDecoder)


class TestMtgDeckDecodeError(TestCase):
    def test___str__(self):
        try:
            raise MtgDeckDecodeError('a')
        except MtgDeckDecodeError as e:
            self.assertEqual("Could not determine encoding format: ('a',)",
                             str(e))


class TestMtgDeckDecoder(TestCase):
    @patch.multiple(MtgDeckDecoder, __abstractmethods__=set())
    def setUp(self):
        self.decoder = MtgDeckDecoder()

    def test_MtgDeckDecoder(self):
        self.assertRaises(TypeError, MtgDeckDecoder)

    def test__gather(self):
        entries = [('section', 'card', 'setid', 1),
                   ('section', 'card', 'setid', 1)]
        expected = {'section': {'card': {'setid': 2}}}
        actual = self.decoder._gather(entries)
        self.assertDictEqual(expected, actual)

    def test_load(self):
        string = ''
        fp = StringIO(string)
        expected = {}
        actual = self.decoder.load(fp)
        self.assertDictEqual(expected, actual)

    def test_loads(self):
        string = ''
        expected = {}
        actual = self.decoder.loads(string)
        self.assertDictEqual(expected, actual)


class TestMtgDeckAutoDecoder(TestCase):
    def setUp(self):
        self.decoder = MtgDeckAutoDecoder()

    def test_loads(self):
        decoders = ['text', 'mws', 'octgn', 'cod']

        strings = [
            """
            1 mname
            Sideboard
            2 sname
            """,

            """
            1 mname
            SB: 2 sname
            """,

            """
            <deck>
              <section name="Main">
                <card qty="1">mname</card>
              </section>
              <section name="Sideboard">
                <card qty="2">sname</card>
              </section>
            </deck>
            """,

            """
            <cockatrice_deck>
              <zone name="main">
                <card number="1" name="mname"/>
              </zone>
              <zone name="board">
                <card number="2" name="sname"/>
              </zone>
            </cockatrice_deck>
            """
        ]

        expected = [
            {'mainboard': {'mname': {None: 1}},
             'Sideboard': {'sname': {None: 2}}},

            {'mainboard': {'mname': {None: 1}},
             'sideboard': {'sname': {None: 2}}},

            {'Main': {'mname': {None: 1}},
             'Sideboard': {'sname': {None: 2}}},

            {'main': {'mname': {None: 1}},
             'board': {'sname': {None: 2}}}
        ]

        actual = [self.decoder.loads(s) for s in strings]

        for d, (a, b) in zip(decoders, zip(expected, actual)):
            self.assertDictEqual(a, b, msg=d)

        with self.assertRaises(MtgDeckDecodeError):
            self.decoder.loads('invalid')


class TestMtgDeckMagicWorkstationDecoder(TestCase):
    def setUp(self):
        self.decoder = MtgDeckMagicWorkstationDecoder()

    def test__decode(self):
        string = """
        1 mname
        SB: 1 sname
        1 [SETID] mname
        SB: 1 [SETID] sname
        """

        expected = [
            ('mainboard', 'mname', None, 1),
            ('sideboard', 'sname', None, 1),
            ('mainboard', 'mname', 'SETID', 1),
            ('sideboard', 'sname', 'SETID', 1),
        ]

        actual = list(self.decoder._decode(string))

        self.assertListEqual(expected, actual)


class TestMtgDeckOCTGNDecoder(TestCase):
    def setUp(self):
        self.decoder = MtgDeckOCTGNDecoder()

    def test__decode(self):
        pass
