from unittest import TestCase

from os import unlink
from sys import (stdin, stdout)
from argparse import Namespace
from mtgdeck.__main__ import (action, main, parse_arguments)
from mtgdeck import (AutoDecoder,
                     TextEncoder,
                     MagicWorkstationDecoder,
                     CockatriceEncoder)


class TestClassAction(TestCase):
    def setUp(self):
        self.decoder_action = action('decoder')
        self.encoder_action = action('encoder')

    def test_action(self):
        self.assertEqual('ClassAction', self.decoder_action.__name__)
        self.assertEqual('ClassAction', self.encoder_action.__name__)

    def test___init__(self):
        decoder_action_obj = self.decoder_action(None, 'dest')

        self.assertCountEqual(
            ['default', 'auto', 'text', 'mws', 'cod', 'octgn'],
            decoder_action_obj.choices
        )
        self.assertEqual(AutoDecoder, decoder_action_obj.default)

        encoder_action_obj = self.encoder_action(None, 'dest')

        self.assertCountEqual(
            ['default', 'text', 'mws', 'cod', 'octgn'],
            encoder_action_obj.choices
        )
        self.assertEqual(TextEncoder, encoder_action_obj.default)

    def test___call__(self):
        ns = Namespace()

        decoder = self.decoder_action(None, 'dest')
        decoder.__call__(None, ns, 'default')
        self.assertEqual(AutoDecoder, ns.dest)

        encoder = self.encoder_action(None, 'dest')
        encoder.__call__(None, ns, 'default')
        self.assertEqual(TextEncoder, ns.dest)


class TestMain(TestCase):
    def setUp(self):
        self.test_input_file = open('input.txt', 'w').name
        self.test_output_file = open('output.txt', 'w').name

    def tearDown(self):
        unlink(self.test_input_file)
        unlink(self.test_output_file)

    def _assertDictEqual(self, d1, d2, msg=None):
        for k, v1 in d1.items():
            self.assertIn(k, d2, msg)
            v2 = d2[k]
            if k in ['input', 'output']:
                self.assertEqual(v1.name, v2.name, msg)
            else:
                self.assertEqual(v1, v2, msg)
        return True

    def test_parse_arguments(self):
        args = [
            ([], {'decoder': AutoDecoder,
                  'encoder': TextEncoder,
                  'input': stdin,
                  'output': stdout}),
            (['-d', 'mws',
              '-e', 'cod',
              '-i', 'input.txt',
              '-o', 'output.txt'],
             {'decoder': MagicWorkstationDecoder,
              'encoder': CockatriceEncoder,
              'input': open('input.txt', 'r'),
              'output': open('output.txt', 'w')})
        ]

        for argv, expected in args:
            actual = vars(parse_arguments(argv))
            self._assertDictEqual(expected, actual)

    def test_main(self):
        with open('input.txt', 'w') as fp:
            fp.write('1 mname\n')

        with self.assertRaises(SystemExit):
            main(['-d', 'mws',
                  '-e', 'cod',
                  '-i', 'input.txt',
                  '-o', 'output.txt'])

        expected = ''.join([_.strip() for _ in """
        <cockatrice_deck>
          <zone name="main">
            <card name="mname" number="1" />
          </zone>
        </cockatrice_deck>""".split('\n')])

        actual = open('output.txt').read()
        self.assertEqual(expected, actual)
