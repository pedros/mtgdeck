from unittest import TestCase
from unittest.mock import patch
from io import StringIO

from mtgdeck.encoder import (MtgDeckEncodeError,
                             MtgDeckEncoder,
                             MtgDeckTextEncoder,
                             MtgDeckMagicWorkstationEncoder,
                             MtgDeckOCTGNEncoder,
                             MtgDeckCockatriceEncoder)


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


class TestMtgDeckTextEncoder(TestCase):
    def setUp(self):
        self.encoder = MtgDeckTextEncoder()

    def test__encode(self):
        obj = [('mname', {'count': 2}),
               ('sname', {'section': 'Sideboard', 'count': 2})]

        expected = """2 mname\nSideboard\n2 sname\n"""

        actual = self.encoder._encode(obj)
        self.assertEqual(expected, actual)


class TestMtgDeckMagicWorkstationEncoder(TestCase):
    def setUp(self):
        self.encoder = MtgDeckMagicWorkstationEncoder()

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


class TestMtgDeckOCTGNEncoder(TestCase):
    def setUp(self):
        self.encoder = MtgDeckOCTGNEncoder()

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


class TestMtgDeckCockatriceEncoder(TestCase):
    def setUp(self):
        self.encoder = MtgDeckCockatriceEncoder()

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
