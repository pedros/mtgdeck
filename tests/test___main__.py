from unittest import TestCase
from unittest.mock import patch

from mtgdeck.__main__ import action
from mtgdeck import (MtgDeckAutoDecoder,
                     MtgDeckTextEncoder)


class TestClassAction(TestCase):
    def setUp(self):
        self.decoder_action = action('decoder')
        self.encoder_action = action('encoder')

    def test_action(self):
        self.assertEqual('ClassAction', self.decoder_action.__name__)
        self.assertEqual('ClassAction', self.encoder_action.__name__)

    def test__ClassAction(self):
        decoder = self.decoder_action(None, 'dest')
        decoder.__call__(None, patch('argparse.Namespace'), 'default')

        self.assertListEqual(
            ['default', 'auto', 'text', 'mws', 'cod', 'octgn'],
            list(decoder.choices)
        )
        self.assertEqual(MtgDeckAutoDecoder, decoder.default)

        encoder = self.encoder_action(None, 'dest')
        encoder.__call__(None, patch('argparse.Namespace'), 'default')

        self.assertListEqual(
            ['default', 'text', 'mws', 'cod', 'octgn'],
            list(encoder.choices)
        )
        self.assertEqual(MtgDeckTextEncoder, encoder.default)
