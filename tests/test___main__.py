from unittest import TestCase

from tempfile import mkdtemp
from os import unlink, path, rmdir
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
        self.test_dir = mkdtemp()
        self.test_input_file = path.join(self.test_dir, 'input.txt')
        self.test_output_file = path.join(self.test_dir, 'output.txt')
        open(self.test_input_file, 'w').close()

    def tearDown(self):
        unlink(self.test_input_file)
        unlink(self.test_output_file)
        rmdir(self.test_dir)

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
        fp_in = open(self.test_input_file, 'r')
        fp_out = open(self.test_output_file, 'w')

        args = [
            ([], {'decoder': AutoDecoder,
                  'encoder': TextEncoder,
                  'input': stdin,
                  'output': stdout}),
            (['-d', 'mws',
              '-e', 'cod',
              '-i', self.test_input_file,
              '-o', self.test_output_file],
             {'decoder': MagicWorkstationDecoder,
              'encoder': CockatriceEncoder,
              'input': fp_in,
              'output': fp_out})
        ]

        for argv, expected in args:
            actual = vars(parse_arguments(argv))
            self._assertDictEqual(expected, actual)

        fp_in.close()
        fp_out.close()

    def test_main(self):
        with open(self.test_input_file, 'w') as fp:
            fp.write('1 mname\n')

        with self.assertRaises(SystemExit):
            main(['-d', 'mws',
                  '-e', 'cod',
                  '-i', self.test_input_file,
                  '-o', self.test_output_file])

        expected = ''.join([_.strip() for _ in """
        <cockatrice_deck>
          <zone name="main">
            <card name="mname" number="1" />
          </zone>
        </cockatrice_deck>""".split('\n')])

        with open(self.test_output_file) as fp:
            actual = fp.read()

        self.assertEqual(expected, actual)
