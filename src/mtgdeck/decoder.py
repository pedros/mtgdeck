"""Decoder implementations for mtgdeck."""
from pyparsing import (Group, Keyword, OneOrMore, Optional, ParserElement,
                       Word, cppStyleComment, empty, nestedExpr, nums,
                       restOfLine)
from .base.decoder import (DecodeError, Decoder, TextDecoder, XMLDecoder)
ParserElement.enablePackrat()


class AutoDecoder(Decoder):
    """Auto-decoding class.

    Determines the input decoding format by try-catching until it succeeds.
    If it fails, raises a ``DecodeError`` exception.

    """

    def _decode(self, string):
        """No-op. Instead, concrete class ``_decode()`` methods are used."""

    def loads(self, string):
        """Try to decode ``string`` with different decoders.

        Raise ``DecodeError`` if all decoders are exhausted.

        """
        exceptions = []
        for cls in (MagicOnlineDecoder, MagicWorkstationDecoder,
                    OCTGNDecoder, CockatriceDecoder):
            try:
                return cls().loads(string)
            except Exception as _:
                exceptions.append((cls, _))
        raise DecodeError(exceptions)


class MagicOnlineDecoder(TextDecoder):
    """Decoding class for the simple text format."""

    comment = cppStyleComment
    section = Group(Keyword('Sideboard'))
    count = Word(nums)
    card = empty + restOfLine
    setid = nestedExpr('[', ']')
    entry = Group(count + card)
    deck = OneOrMore(comment | section | entry).ignore(comment)

    def decode_entry(self, entry):
        """Return (card name (str), attributes (dict)) from ``entry``."""
        if len(entry) == 1 and entry[0] == 'Sideboard':
            setattr(self, 'sideboard', True)
            return None
        else:
            count, card = entry
            attrs = {'count': int(count)}
            if getattr(self, 'sideboard', False):
                attrs['section'] = 'Sideboard'
            return card, attrs


class MagicWorkstationDecoder(TextDecoder):
    """Decoding class for the Magic Workstation format."""

    comment = cppStyleComment
    section = Group(Keyword('SB:'))
    count = Word(nums)
    setid = nestedExpr('[', ']')
    card = empty + restOfLine
    entry = Group(Optional(section, None) +
                  count +
                  Optional(setid, []) +
                  card)
    deck = OneOrMore(comment | entry).ignore(comment)

    def decode_entry(self, entry):
        """Return (card name (str), attributes (dict)) from ``entry``."""
        section, count, setid, card = entry
        attrs = {'count': int(count)}
        if setid:
            attrs['setid'] = setid[0]
        if section:
            attrs['section'] = 'Sideboard'
        return card, attrs


class OCTGNDecoder(XMLDecoder):
    """Decoding class for the OCTGN Deck Creator format."""

    root = 'deck'
    section = 'section'
    count = 'qty'


class CockatriceDecoder(XMLDecoder):
    """Decoding class for the Cockatrice format."""

    root = 'cockatrice_deck'
    section = 'zone'
    count = 'number'
