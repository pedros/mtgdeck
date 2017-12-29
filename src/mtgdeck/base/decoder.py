"""Abstract base decoder classes."""
from abc import ABCMeta, abstractmethod
from io import StringIO
from defusedxml.ElementTree import parse  # pylint: disable=E0401


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


class TextDecoder(Decoder):
    """Abstract base class for text-based decoders.

    Decoders are expected to set the ``deck`` property, and override the
    ``decode_entry`` method.

    """

    @property
    @abstractmethod
    def deck(self):
        """Pyparsing parser that should consume the full input string.

        ``OneOrMore``-wrapped pyparsing parser capable of consuming the full
        input string.

        """

    @abstractmethod
    def decode_entry(self, entry):
        """Extract and return from ``entry`` a (card name (str), attributes
        (dict)).

        ``entry`` is a tuple argument (as returned by the ``parseString``
        method on ``deck``.)

        """

    def _decode(self, string):
        """Decode ``string``, yielding (card name (str), attributes (dict))."""
        entries = self.deck.parseString(string, parseAll=True)

        for entry in entries:
            parsed_entry = self.decode_entry(entry)
            if parsed_entry:
                yield parsed_entry


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
                card = entry.attrib.get('name', entry.text)
                if not card:
                    raise DecodeError("Missing a card entry 'name'")
                yield card, {'section': section.attrib['name'],
                             'count': int(count)}
