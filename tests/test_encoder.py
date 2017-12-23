from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from mtgdeck.encoder import (EncodeError,
                             Encoder,
                             XMLEncoder,
                             MagicOnlineEncoder,
                             MagicWorkstationEncoder,
                             OCTGNEncoder,
                             CockatriceEncoder)


class TestEncodeError(TestCase):
    def test___str__(self):
        try:
            raise EncodeError('a')
        except EncodeError as e:
            self.assertEqual("Could not determine encoding format: ('a',)",
                             str(e))


class TestEncoder(TestCase):
    @patch.multiple(Encoder, __abstractmethods__=set())
    def setUp(self):
        self.encoder = Encoder()

    def test_Encoder(self):
        self.assertRaises(TypeError, Encoder)

    def test_dump(self):
        obj = []
        fp = StringIO()
        expected = ''
        self.encoder.dump(obj, fp)
        actual = fp.read()
        self.assertEqual(expected, actual)

    def test_dumps(self):
        obj = []
        expected = ''
        actual = self.encoder.dumps(obj)
        self.assertEqual(expected, actual)


class TestMagicOnlineEncoder(TestCase):
    def setUp(self):
        self.encoder = MagicOnlineEncoder()

    def test__encode(self):
        obj = [('mname', {'count': 2}),
               ('sname', {'section': 'Sideboard', 'count': 2}),
               ('sname', {'section': 'Sideboard', 'count': 2})]

        expected = """2 mname\nSideboard\n2 sname\n2 sname\n"""
        actual = self.encoder._encode(obj)
        self.assertEqual(expected, actual)

        obj = [('mname', {'count': 2})]

        expected = """2 mname\n"""
        actual = self.encoder._encode(obj)
        self.assertEqual(expected, actual)


class TestMagicWorkstationEncoder(TestCase):
    def setUp(self):
        self.encoder = MagicWorkstationEncoder()

    def test__encode(self):
        obj = [('mname', {'count': 1}),
               ('mname', {'count': 1, 'setid': 'SETID'}),
               ('sname', {'section': 'sideboard', 'count': 1}),
               ('sname', {'section': 'sideboard', 'count': 1,
                          'setid': 'SETID'})]

        expected = """1 mname\n1 [SETID] mname
SB: 1 sname\nSB: 1 [SETID] sname\n"""

        actual = self.encoder._encode(obj)
        self.assertEqual(expected, actual)


class TestXMLEncoder(TestCase):
    def test__set_content(self):
        class BadXMLEncoder(XMLEncoder):
            root = 'deck'
            section = 'section'
            section_name = 'Main'
            count = 'qty'
            content = 'bad value'

        with self.assertRaises(EncodeError):
            BadXMLEncoder()._encode([('mname', {'count': 1})])


class TestOCTGNEncoder(TestCase):
    def setUp(self):
        self.encoder = OCTGNEncoder()

    def test__encode(self):
        obj = [('mname', {'count': 1}),
               ('mname', {'count': 2, 'setid': 'SETID'}),
               ('sname', {'section': 'Sideboard', 'count': 2})]

        expected = ''.join([_.strip() for _ in """
        <deck>
          <section name="Main">
            <card qty="1">mname</card>
            <card qty="2" setid="SETID">mname</card>
          </section>
          <section name="Sideboard">
            <card qty="2">sname</card>
          </section>
        </deck>""".split('\n')])

        actual = self.encoder._encode(obj)
        self.assertEqual(expected, actual)


class TestCockatriceEncoder(TestCase):
    def setUp(self):
        self.encoder = CockatriceEncoder()

    def test__encode(self):
        obj = [('mname', {'count': 1}),
               ('mname', {'count': 2, 'setid': 'SETID'}),
               ('sname', {'section': 'board', 'count': 2})]

        # NOTE(psilva): this assertion is way too sensitive to whitespace,
        # assumed dictionary order of attributes, etc. It's difficult to
        # do better without monkey-patching the etree xml builder/serializer
        expected = ''.join([_.strip() for _ in """
        <cockatrice_deck>
          <zone name="main">
            <card name="mname" number="1" />
            <card name="mname" number="2" setid="SETID" />
          </zone>
          <zone name="board">
            <card name="sname" number="2" />
          </zone>
        </cockatrice_deck>""".split('\n')])

        actual = self.encoder._encode(obj)
        self.assertEqual(expected, actual)
