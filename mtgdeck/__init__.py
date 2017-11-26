__version__ = '0.0.1'

__author__ = 'Pedro Silva <psilva+git@pedrosilva.pt>'

__all__ = [
    'load', 'loads',
    'MtgDeckAutoDecoder', 'MtgDeckDecodeError'
]


from .decoder import MtgDeckAutoDecoder, MtgDeckDecodeError


def load(fp):
    return loads(fp.read())


def loads(string):
    return MtgDeckAutoDecoder._loads(string)
