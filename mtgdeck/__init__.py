"""Public API entry-point for mtgdeck"""

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


__version__ = '0.1'
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


def load(fp, cls=MtgDeckAutoDecoder):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing an
    MTG decklist) to a Python object.

    To use a custom ``MTGDeckDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``MtgDeckAutoDecoder`` is used.

    """
    return cls().load(fp)


def loads(string, cls=MtgDeckAutoDecoder):
    """Deserialize ``string`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing an MTG decklist) to a Python object.

    To use a custom ``MTGDeckDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``MtgDeckAutoDecoder`` is used.

    """
    return cls().loads(string)


def dump(obj, fp, cls=MtgDeckTextEncoder):
    """Serialize ``obj`` as a MTG decklist formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    To use a custom ``MtgDeckEncoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``MtgDeckEncoder`` is used.

    """
    return cls().dump(obj, fp)


def dumps(obj, cls=MtgDeckTextEncoder):
    """Serialize ``obj`` to a MTG decklist formatted ``str``.

    To use a custom ``MtgDeckEncoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``MtgDeckEncoder`` is used.

    """
    return cls().dumps(obj)
