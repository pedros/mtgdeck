__version__ = '0.0.1'
__author__ = 'Pedro Silva <psilva+git@pedrosilva.pt>'
__all__ = [
    'load', 'loads',
    'dump', 'dumps',
    'MtgDeckDecodeError',
    'MtgDeckAutoDecoder',
    'MtgDeckTextDecoder',
    'MtgDeckMagicWorkstationDecoder',
    'MtgDeckOCTGNDecoder',
    'MtgDeckCockatriceDecoder',
    'MtgDeckEncodeError',
    'MtgDeckTextEncoder',
    'MtgDeckMagicWorkstationEncoder',
    'MtgDeckOCTGNEncoder',
    'MtgDeckCockatriceEncoder',
]

from .decoder import (MtgDeckDecodeError,
                      MtgDeckAutoDecoder,
                      MtgDeckTextDecoder,
                      MtgDeckMagicWorkstationDecoder,
                      MtgDeckOCTGNDecoder,
                      MtgDeckCockatriceDecoder)

from .encoder import (MtgDeckEncodeError,
                      MtgDeckTextEncoder,
                      MtgDeckMagicWorkstationEncoder,
                      MtgDeckOCTGNEncoder,
                      MtgDeckCockatriceEncoder)


def load(fp, cls=MtgDeckAutoDecoder):
    return cls().load(fp)


def loads(string, cls=MtgDeckAutoDecoder):
    return cls().loads(string)


def dump(obj, fp, cls=MtgDeckTextEncoder):
    return cls().dump(obj, fp)


def dumps(obj, cls=MtgDeckTextEncoder):
    return cls().dumps(obj)
