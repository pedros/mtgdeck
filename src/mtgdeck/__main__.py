"""mtgdeck - MTG deck list decoder and encoder library and application

"""
import sys
import argparse

import mtgdeck


ENCODECS = {
    'decoder': {'default': mtgdeck.AutoDecoder,
                'auto': mtgdeck.AutoDecoder,
                'text': mtgdeck.MagicOnlineDecoder,
                'mws': mtgdeck.MagicWorkstationDecoder,
                'cod': mtgdeck.CockatriceDecoder,
                'octgn': mtgdeck.OCTGNDecoder},
    'encoder': {'default': mtgdeck.MagicOnlineEncoder,
                'text': mtgdeck.MagicOnlineEncoder,
                'mws': mtgdeck.MagicWorkstationEncoder,
                'cod': mtgdeck.CockatriceEncoder,
                'octgn': mtgdeck.OCTGNEncoder},
}


def action(kind):
    """Return a ClassAction(argparse.Action) for ``kind``."""

    class ClassAction(argparse.Action):  # pylint: disable=R0903
        """Map argument string values to a class in module ``kind``.

        Set appropriate ``choices`` and ``default`` attributes.

        """
        def __init__(self, *args, **kwargs):
            kwargs['choices'] = ENCODECS[kind].keys()
            kwargs['default'] = ENCODECS[kind]['default']
            super(ClassAction, self).__init__(*args, **kwargs)

        def __call__(self, parser, namespace, value, option_string=None):
            """Coerce argument value to the appropriate ``kind`` class."""
            setattr(namespace, self.dest, ENCODECS[kind][value])

    return ClassAction


def parse_arguments(argv):
    """Parse command line arguments and return a Namespace object."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--decoder', help='decoding format',
                        action=action('decoder'))
    parser.add_argument('-e', '--encoder', help='encoding format',
                        action=action('encoder'))
    parser.add_argument('-i', '--input', help='input file',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--output', help='output file',
                        type=argparse.FileType('w'), default=sys.stdout)
    return parser.parse_args(argv)


def main(argv=None):
    """Run a full encode-decode pipeline."""
    args = parse_arguments(argv)
    mtgdeck.dump(mtgdeck.load(args.input, cls=args.decoder),
                 args.output,
                 cls=args.encoder)
    args.input.close()
    args.output.close()
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])
