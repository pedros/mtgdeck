"""mtgdeck - MTG deck list decoder and encoder library and application

"""
import sys
import argparse

import mtgdeck


def action(kind):
    """Return a ClassAction(argparse.Action) for ``kind``."""
    encodecs = {
        'decoder': {'default': mtgdeck.AutoDecoder,
                    'auto': mtgdeck.AutoDecoder,
                    'text': mtgdeck.TextDecoder,
                    'mws': mtgdeck.MagicWorkstationDecoder,
                    'cod': mtgdeck.CockatriceDecoder,
                    'octgn': mtgdeck.OCTGNDecoder},
        'encoder': {'default': mtgdeck.TextEncoder,
                    'text': mtgdeck.TextEncoder,
                    'mws': mtgdeck.MagicWorkstationEncoder,
                    'cod': mtgdeck.CockatriceEncoder,
                    'octgn': mtgdeck.OCTGNEncoder},
    }

    class ClassAction(argparse.Action):
        """Map argument string values to a class in module ``kind``.

        Set appropriate ``choices`` and ``default`` attributes.

        """
        def __init__(self, *args, **kwargs):
            kwargs['choices'] = encodecs[kind].keys()
            kwargs['default'] = encodecs[kind]['default']
            super(ClassAction, self).__init__(*args, **kwargs)

        def __call__(self, parser, namespace, value, option_string=None):
            """Coerce argument value to the appropriate ``kind`` class."""
            setattr(namespace, self.dest, encodecs[kind][value])

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
    args = parse_arguments(argv)
    sys.exit(mtgdeck.dump(mtgdeck.load(args.input, cls=args.decoder),
                          args.output,
                          cls=args.encoder))


if __name__ == '__main__':
    main(sys.argv[1:])
