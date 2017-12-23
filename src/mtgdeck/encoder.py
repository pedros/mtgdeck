"""Encoder implementations for mtgdeck."""
from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import Element, SubElement, tostring  # nosec


class EncodeError(Exception):
    """Format encoding exception."""
    def __str__(self):
        return 'Could not determine encoding format: {}'.format(self.args)


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


class MagicOnlineEncoder(Encoder):
    """Encoding class for the simple text format.

    This is the format that MTGO outputs. Each line has the form 'quantity
    name'. An optional line containing the word 'Sideboard' indicates that
    subsequent entries are sideboard material.

    """
    def _encode(self, obj):
        out = ''
        sideboard = False
        for name, attrs in obj:
            if attrs.get('section', False) == 'Sideboard':
                if not sideboard:
                    out += 'Sideboard\n'
                    sideboard = True
            out += '{} {}\n'.format(attrs['count'], name)
        return out


class MagicWorkstationEncoder(Encoder):
    """Encoding class for the Magic Workstation format.

    Each line has the form '[SB: ]quantity [SETID ]name', '[]' meaning optional
    fields.

    """
    def _encode(self, obj):
        out = ''

        for name, attrs in obj:
            entries = []
            if 'section' in attrs:
                entries.append('SB:')

            entries.append(str(attrs['count']))

            if 'setid' in attrs:
                entries.append('[{}]'.format(attrs['setid']))

            entries.append('{}\n'.format(name))
            out += ' '.join(entries)

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
    def section_name(self):
        """Section name(ie: sideboard) tag for the XML encoding format."""

    @property
    @abstractmethod
    def count(self):
        """Quantity (ie: qty, number) tag for the XML encoding format."""

    @property
    @abstractmethod
    def content(self):
        """How to set card name in card ``Element`` ('attrib' or 'text')."""

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
            if self.content == 'text':
                card.text = name
            elif self.content == 'attrib':
                card.attrib['name'] = name
            else:
                raise EncodeError('invalid content: "{}"'.format(self.content))

        return tostring(root, encoding='unicode')


class OCTGNEncoder(XMLEncoder):
    """Encoding class for the OCTGN Deck Creator format."""
    root = 'deck'
    section = 'section'
    section_name = 'Main'
    count = 'qty'
    content = 'text'


class CockatriceEncoder(XMLEncoder):
    """Encoding class for the Cockatrice format."""
    root = 'cockatrice_deck'
    section = 'zone'
    section_name = 'main'
    count = 'number'
    content = 'attrib'
