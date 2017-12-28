"""Decoder implementations for mtgdeck."""
from abc import ABCMeta, abstractmethod
from io import StringIO
from pyparsing import (Group, Keyword, OneOrMore, Optional, ParseException,
                       ParserElement, Word, cppStyleComment, empty, nestedExpr,
                       nums, restOfLine)
from defusedxml.ElementTree import (parse, ParseError)  # pylint: disable=E0401


class DecodeError(Exception):
    """Format decoding exception."""

    def __str__(self):
        return 'Could not determine decoding format: {}'.format(self.args)


class Decoder(metaclass=ABCMeta):
    """Abstract base class for decoders.

    Decoders are expected to implement a single method, ``_decode()``.

    """
    @abstractmethod
    def _decode(self, string):
        """Decode ``string`` into an internal representation format.

        Return a sequence of ``(card name (str), attributes (dict))``.

        """

        return []

    def load(self, fin):
        """Deserialize ``fin`` (a ``.read()``-supporting file-like object
        containing an MTG decklist) to a Python object.

        """
        return self.loads(fin.read())

    def loads(self, string):
        """Deserialize ``string`` (a ``str``, ``bytes`` or ``bytearray`` instance
        containing an MTG decklist) to a Python object.

        """
        src = string.replace('\r\n', '\n').replace('\r', '\n')
        return list(self._decode(src))


class AutoDecoder(Decoder):
    """Auto-decoding class.

    Determines the input decoding format by try-catching until it succeeds.
    If it fails, raises a ``DecodeError`` exception.

    """

    def _decode(self, string):
        """No-op. Instead, concrete class ``_decode()`` methods are used."""
        pass

    def loads(self, string):
        """Try to decode ``string`` with different decoders.

        Raise ``DecodeError`` if all decoders are exhausted.

        """
        exceptions = []
        for cls in (MagicOnlineDecoder, MagicWorkstationDecoder,
                    OCTGNDecoder, CockatriceDecoder):
            try:
                return cls().loads(string)
            except (ParseException, ParseError, KeyError) as _:
                exceptions.append((cls, _))
        raise DecodeError(exceptions)


class MagicOnlineDecoder(Decoder):
    """Decoding class for the simple text format."""

    def __init__(self):
        """Set a pyparsing grammar."""
        self.comment = cppStyleComment
        self.section = Keyword('Sideboard')
        self.count = Word(nums)
        self.card = empty + restOfLine
        self.entry = Group(self.count + self.card)
        self.deck = OneOrMore(self.comment |
                              self.section |
                              self.entry).ignore(self.comment)

    def _decode(self, string):
        """Decode ``string``, yielding (card name (str), attributes (dict))."""
        entries = self.deck.parseString(string, parseAll=True)
        section = None
        for entry in entries:
            if len(entry) != 2:
                section = entry
            else:
                count, card = entry
                if section == 'Sideboard':
                    yield card, {'section': 'Sideboard', 'count': int(count)}
                else:
                    yield card, {'count': int(count)}


class MagicWorkstationDecoder(Decoder):
    """Decoding class for the Magic Workstation format."""

    def __init__(self):
        """Set a pyparsing grammar."""

        ParserElement.enablePackrat()

        self.comment = cppStyleComment
        self.section = Keyword('SB:')
        self.count = Word(nums)
        self.set = nestedExpr('[', ']')
        self.card = empty + restOfLine
        self.entry = Group(Optional(self.section, None) +
                           self.count +
                           Optional(self.set, []) +
                           self.card)
        self.deck = OneOrMore(self.comment | self.entry).ignore(self.comment)

    def _decode(self, string):
        """Decode ``string``, yielding (card name (str), attributes (dict))."""
        entries = self.deck.parseString(string)
        for entry in entries:
            section, count, setid, card = entry

            attrs = {'count': int(count)}

            if setid:
                attrs['setid'] = setid[0]
            if section:
                attrs['section'] = 'Sideboard'

            yield card, attrs


class XMLDecoder(Decoder):
    """Abstract base class for XML-based decoders.

    Decoders are expected to set the ``root``, ``section`` and ``count``
    properties.

    """

    @property
    @abstractmethod
    def root(self):
        """Root (top-level) tag for the XML decoding format."""

    @property
    @abstractmethod
    def section(self):
        """Section (ie: sideboard) tag for the XML decoding format."""

    @property
    @abstractmethod
    def count(self):
        """Quantity (ie: qty, number) tag for the XML decoding format."""

    def _decode(self, string):
        """Decode ``string``, yielding (card name (str), attributes (dict))."""
        tree = parse(StringIO(string))

        if tree.getroot().tag != self.root:
            raise KeyError('Missing a "{}" tag'.format(self.root))

        for section in tree.findall(self.section):
            for entry in section.findall('card'):
                count = entry.attrib[self.count]
                card = entry.text
                if not card:
                    card = entry.attrib.get('name', False)
                    if not card:
                        raise DecodeError("Missing a card entry 'name'")
                yield card, {'section': section.attrib['name'],
                             'count': int(count)}


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
