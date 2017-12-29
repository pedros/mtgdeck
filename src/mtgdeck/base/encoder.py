"""Abstract base encoder classes."""
from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import Element, SubElement, tostring  # nosec


class Encoder(metaclass=ABCMeta):
    """Abstract base class for encoders.

    Encoders are expected to implement a single method, ``_encode()``.

    """

    @abstractmethod
    def _encode(self, obj):
        """Encode ``obj`` into a public representation format.

        ``obj`` is a sequence of ``(card name (str), attributes (dict))``.
        Returns a ``string``.

        """

        return ''

    def dump(self, obj, fout):
        """Serialize ``obj`` as a MTG decklist formatted stream to ``fout`` (a
        ``.write()``-supporting file-like object).

        """
        fout.write(self.dumps(obj))

    def dumps(self, obj):
        """Serialize ``obj`` to a MTG decklist formatted ``str``."""
        return self._encode(obj)


class TextEncoder(Encoder):
    """Abstract base class for text-based encoders.

    Encoders are expected to override the ``encode_entry`` method.

    """

    @abstractmethod
    def encode_entry(self, name, attrs):
        """Build and return from ``name`` and ``attrs`` an encoded entry string.

        (``name``, ``attrs``) is a tuple argument (str, dict).

        """

    def _encode(self, obj):
        out = ''
        for name, attrs in obj:
            out += self.encode_entry(name, attrs)
        return out


class XMLEncoder(Encoder):
    """Abstract base class for XML-based encoders.

    Encoders are expected to set the ``root``, ``section``, ``section_name``
    and ``count`` properties, and the ``set_content`` method.

    """

    @property
    @abstractmethod
    def root(self):
        """Root (top-level) tag for the XML encoding format."""

    @property
    @abstractmethod
    def section(self):
        """Section (ie: sideboard, etc) tag for the XML encoding format."""

    @property
    @abstractmethod
    def count(self):
        """Quantity (ie: qty, number) tag for the XML encoding format."""

    @property
    @abstractmethod
    def section_name(self):
        """Section name(ie: sideboard) tag for the XML encoding format."""

    @abstractmethod
    def set_content(self, card, name):
        """Set ``name`` in ``card``.

        ``card`` is an ``ElementTree.Element``, and ``name`` should be set
        either as an attribute (``card.attribs['key']``) or as the text node
        (``card.text``).

        """

    def _encode(self, obj):
        root = Element(self.root)
        sections = {}

        for name, attrs in obj:
            section = attrs.get('section', self.section_name)
            setid = attrs.get('setid', None)
            count = attrs['count']

            if section not in sections:
                sections[section] = SubElement(root, self.section,
                                               {'name': section})

            attrs = {self.count: str(count)}
            if setid:
                attrs['setid'] = setid

            card = SubElement(sections[section], 'card', attrs)
            self.set_content(card, name)

        return tostring(root, encoding='unicode')
