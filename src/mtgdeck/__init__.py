"""Public API entry-point for mtgdeck."""

from .decoder import (DecodeError,
                      AutoDecoder,
                      MagicOnlineDecoder,
                      MagicWorkstationDecoder,
                      OCTGNDecoder,
                      CockatriceDecoder)

from .encoder import (EncodeError,
                      MagicOnlineEncoder,
                      MagicWorkstationEncoder,
                      OCTGNEncoder,
                      CockatriceEncoder)


__version__ = '0.1.0'
__author__ = 'Pedro Silva <psilva+git@pedrosilva.pt>'
__all__ = [
    'load', 'loads',
    'dump', 'dumps',
    'DecodeError',
    'AutoDecoder',
    'MagicOnlineDecoder',
    'MagicWorkstationDecoder',
    'OCTGNDecoder',
    'CockatriceDecoder',
    'EncodeError',
    'MagicOnlineEncoder',
    'MagicWorkstationEncoder',
    'OCTGNEncoder',
    'CockatriceEncoder',
]


def load(fin, cls=AutoDecoder):
    """Deserialize ``fin`` (a ``.read()``-supporting file-like object containing an
    MTG decklist) to a Python object.

    To use a custom ``MTGDeckDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``AutoDecoder`` is used.

    """
    return cls().load(fin)


def loads(string, cls=AutoDecoder):
    """Deserialize ``string`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing an MTG decklist) to a Python object.

    To use a custom ``MTGDeckDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``AutoDecoder`` is used.

    """
    return cls().loads(string)


def dump(obj, fout, cls=MagicOnlineEncoder):
    """Serialize ``obj`` as a MTG decklist formatted stream to ``fout`` (a
    ``.write()``-supporting file-like object).

    To use a custom ``Encoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``Encoder`` is used.

    """
    return cls().dump(obj, fout)


def dumps(obj, cls=MagicOnlineEncoder):
    """Serialize ``obj`` to a MTG decklist formatted ``str``.

    To use a custom ``Encoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``Encoder`` is used.

    """
    return cls().dumps(obj)
