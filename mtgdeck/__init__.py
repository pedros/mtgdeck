"""Public API entry-point for mtgdeck."""

from .decoder import (DecodeError,
                      AutoDecoder,
                      TextDecoder,
                      MagicWorkstationDecoder,
                      OCTGNDecoder,
                      CockatriceDecoder)

from .encoder import (EncodeError,
                      TextEncoder,
                      MagicWorkstationEncoder,
                      OCTGNEncoder,
                      CockatriceEncoder)


__version__ = '0.0.6'
__author__ = 'Pedro Silva <psilva+git@pedrosilva.pt>'
__all__ = [
    'load', 'loads',
    'dump', 'dumps',
    'DecodeError',
    'AutoDecoder',
    'TextDecoder',
    'MagicWorkstationDecoder',
    'OCTGNDecoder',
    'CockatriceDecoder',
    'EncodeError',
    'TextEncoder',
    'MagicWorkstationEncoder',
    'OCTGNEncoder',
    'CockatriceEncoder',
]


def load(fp, cls=AutoDecoder):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing an
    MTG decklist) to a Python object.

    To use a custom ``MTGDeckDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``AutoDecoder`` is used.

    """
    return cls().load(fp)


def loads(string, cls=AutoDecoder):
    """Deserialize ``string`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing an MTG decklist) to a Python object.

    To use a custom ``MTGDeckDecoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``AutoDecoder`` is used.

    """
    return cls().loads(string)


def dump(obj, fp, cls=TextEncoder):
    """Serialize ``obj`` as a MTG decklist formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    To use a custom ``Encoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``Encoder`` is used.

    """
    return cls().dump(obj, fp)


def dumps(obj, cls=TextEncoder):
    """Serialize ``obj`` to a MTG decklist formatted ``str``.

    To use a custom ``Encoder`` subclass, specify it with the ``cls``
    kwarg; otherwise ``Encoder`` is used.

    """
    return cls().dumps(obj)
