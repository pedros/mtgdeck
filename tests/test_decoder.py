from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from mtgdeck.decoder import (DecodeError,
                             Decoder,
                             AutoDecoder,
                             MagicWorkstationDecoder,
                             OCTGNDecoder)


class TestDecodeError(TestCase):
    def test___str__(self):
        try:
            raise DecodeError('a')
        except DecodeError as e:
            self.assertEqual("Could not determine decoding format: ('a',)",
                             str(e))


class TestDecoder(TestCase):
    @patch.multiple(Decoder, __abstractmethods__=set())
    def setUp(self):
        self.decoder = Decoder()

    def test_Decoder(self):
        self.assertRaises(TypeError, Decoder)

    def test_load(self):
        string = ''
        fp = StringIO(string)
        expected = []
        actual = self.decoder.load(fp)
        self.assertListEqual(expected, actual)

    def test_loads(self):
        string = ''
        expected = []
        actual = self.decoder.loads(string)
        self.assertListEqual(expected, actual)


class TestAutoDecoder(TestCase):
    def setUp(self):
        self.decoder = AutoDecoder()

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
            [('mname', {'count': 1}),
             ('sname', {'section': 'Sideboard', 'count': 2})],
            [('mname', {'count': 1}),
             ('sname', {'section': 'Sideboard', 'count': 2})],
            [('mname', {'section': 'Main', 'count': 1}),
             ('sname', {'section': 'Sideboard', 'count': 2})],
            [('mname', {'section': 'main', 'count': 1}),
             ('sname', {'section': 'board', 'count': 2})]
        ]

        actual = [self.decoder.loads(s) for s in strings]

        for d, (a, b) in zip(decoders, zip(expected, actual)):
            self.assertListEqual(a, b, msg=d)

        with self.assertRaises(DecodeError):
            self.decoder.loads('invalid')


class TestMagicWorkstationDecoder(TestCase):
    def setUp(self):
        self.decoder = MagicWorkstationDecoder()

    def test__decode(self):
        string = """
        1 mname
        SB: 1 sname
        1 [SETID] mname
        SB: 1 [SETID] sname
        SB: 2 [] sname
        """

        expected = [
            ('mname', {'count': 1}),
            ('sname', {'section': 'Sideboard', 'count': 1}),
            ('mname', {'count': 1, 'setid': 'SETID'}),
            ('sname', {'section': 'Sideboard', 'count': 1, 'setid': 'SETID'}),
            ('sname', {'section': 'Sideboard', 'count': 2}),
        ]

        actual = list(self.decoder._decode(string))

        self.assertListEqual(expected, actual)


class TestOCTGNDecoder(TestCase):
    def setUp(self):
        self.decoder = OCTGNDecoder()

    def test__decode(self):
        pass
