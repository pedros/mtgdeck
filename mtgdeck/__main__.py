import sys
import argparse

import mtgdeck


encodecs = {
    'decoder': {'auto': mtgdeck.MtgDeckAutoDecoder,
                'text': mtgdeck.MtgDeckTextDecoder,
                'mws': mtgdeck.MtgDeckMagicWorkstationDecoder,
                'cod': mtgdeck.MtgDeckCockatriceDecoder,
                'octgn': mtgdeck.MtgDeckOCTGNDecoder},
    'encoder': {'text': mtgdeck.MtgDeckTextEncoder,
                'mws': mtgdeck.MtgDeckMagicWorkstationEncoder,
                'cod': mtgdeck.MtgDeckCockatriceEncoder,
                'octgn': mtgdeck.MtgDeckOCTGNEncoder},
}


def parse_arguments():
    def action(kind):
        class ClassAction(argparse.Action):
            def __call__(self, parser, namespace, value, option_string=None):
                setattr(namespace, self.dest, encodecs[kind][value])
        return ClassAction

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--decoder', help='decoding format',
                        action=action('decoder'), default='auto',
                        choices=encodecs['decoder'].keys())
    parser.add_argument('-e', '--encoder', help='encoding format',
                        action=action('encoder'), default='text',
                        choices=encodecs['encoder'].keys())
    parser.add_argument('-i', '--input', help='input file',
                        type=argparse.FileType, default=sys.stdin)
    parser.add_argument('-o', '--output', help='output file',
                        type=argparse.FileType, default=sys.stdout)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    mtgdeck.dump(
        mtgdeck.load(args.input, cls=args.decoder),
        args.output,
        cls=args.encoder
    )
