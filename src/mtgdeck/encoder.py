from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import Element, SubElement, tostring  # nosec


class EncodeError(Exception):
    def __str__(self):
        return 'Could not determine encoding format: {}'.format(self.args)


class Encoder(metaclass=ABCMeta):
    """Abstract base class for encoders.

    Only one method must be implemented: ``_encode``

    """

    @abstractmethod
    def _encode(self, obj):
        return ''

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj):
        return self._encode(obj)


class MagicOnlineEncoder(Encoder):
    """Encoding class for the simple text format.

    This is the format that MTGO outputs. Each line has the form 'quantity
    name'. An optional line containing the word 'Sideboard' indicates that
    subsequent entries are sideboard material.

    """

    def _encode(self, obj):
        out = ''
        for name, attrs in obj:
            if attrs.get('section', False) == 'Sideboard':
                out += 'Sideboard\n'
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
    @property
    @abstractmethod
    def root(self):
        """Root (top-level) tag for the XML format."""

    @property
    @abstractmethod
    def section(self):
        """Section (ie: sideboard, etc) tag for the XML format."""

    @property
    @abstractmethod
    def section_name(self):
        """Section name(ie: Main, Sideboard) tag for the XML format."""

    @property
    @abstractmethod
    def count(self):
        """Quantity (ie: qty, number) tag for the XML format."""

    @abstractmethod
    def set_content(self, name, card):
        """Set card name in card ``Element``."""

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
            self.set_content(name, card)

        return tostring(root, encoding='unicode')


class OCTGNEncoder(XMLEncoder):
    """Encoding class for the OCTGN Deck Creator format.

    """
    root = 'deck'
    section = 'section'
    section_name = 'Main'
    count = 'qty'

    def set_content(self, name, card):
        card.text = name


class CockatriceEncoder(XMLEncoder):
    """Encoding class for the Cockatrice format.

    """
    root = 'cockatrice_deck'
    section = 'zone'
    section_name = 'main'
    count = 'number'

    def set_content(self, name, card):
        card.attrib['name'] = name
