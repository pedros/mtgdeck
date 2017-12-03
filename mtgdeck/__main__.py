"""mtgdeck - MTG deck list decoder and encoder
"""
import sys
import argparse

import mtgdeck


def action(kind):
    """Return a ClassAction(argparse.Action) for ``kind``."""
    encodecs = {
        'decoder': {'default': mtgdeck.MtgDeckAutoDecoder,
                    'auto': mtgdeck.MtgDeckAutoDecoder,
                    'text': mtgdeck.MtgDeckTextDecoder,
                    'mws': mtgdeck.MtgDeckMagicWorkstationDecoder,
                    'cod': mtgdeck.MtgDeckCockatriceDecoder,
                    'octgn': mtgdeck.MtgDeckOCTGNDecoder},
        'encoder': {'default': mtgdeck.MtgDeckTextEncoder,
                    'text': mtgdeck.MtgDeckTextEncoder,
                    'mws': mtgdeck.MtgDeckMagicWorkstationEncoder,
                    'cod': mtgdeck.MtgDeckCockatriceEncoder,
                    'octgn': mtgdeck.MtgDeckOCTGNEncoder},
    }

    class ClassAction(argparse.Action):
        """Map argument string values to a class in module ``kind``."""

        def __call__(self, parser, namespace, value, option_string=None):
            """Coerce argument value to the appropriate ``kind`` class."""
            setattr(namespace, self.dest, encodecs[kind][value])

        @staticmethod
        def choices():
            """Return all possible ``kind`` strings."""
            return encodecs[kind].keys()

        @staticmethod
        def default():
            """Return default ``kind``."""
            return encodecs[kind]['default']

    return ClassAction


def parse_arguments():
    """Parse command line arguments and return a Namespace object."""
    decoder_action = action('decoder')
    encoder_action = action('encoder')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--decoder', help='decoding format',
                        action=decoder_action,
                        default=decoder_action.default(),
                        choices=decoder_action.choices())
    parser.add_argument('-e', '--encoder', help='encoding format',
                        action=encoder_action,
                        default=encoder_action.default(),
                        choices=encoder_action.choices())
    parser.add_argument('-i', '--input', help='input file',
                        type=argparse.FileType(), default=sys.stdin)
    parser.add_argument('-o', '--output', help='output file',
                        type=argparse.FileType(), default=sys.stdout)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    print(args)
    mtgdeck.dump(mtgdeck.load(args.input, cls=args.decoder),
                 args.output,
                 cls=args.encoder)
