from abc import ABCMeta, abstractmethod
from xml.etree import ElementTree


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


class TextEncoder(Encoder):
    """Encoding class for the simple text format.

    This is the format that MTGO outputs. Each line has the form 'quantity
    name'. An optional line containing the word 'Sideboard' indicates that
    subsequent entries are sideboard material.

    """

    def _encode(self, obj):
        out = ''
        for name, attrs in obj:
            if 'section' in attrs:
                if attrs['section'] == 'Sideboard':
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


class OCTGNEncoder(Encoder):
    """Encoding class for the OCTGN Deck Creator format.

    """
    def _encode(self, obj):
        root = ElementTree.Element('deck')
        sections = {}

        for name, attrs in obj:
            section = attrs.get('section', 'Main')
            setid = attrs.get('setid', None)
            count = attrs['count']
            if section not in sections:
                sections[section] = ElementTree.SubElement(root, 'section',
                                                           {'name': section})

            attrs = {'qty': str(count)}
            if setid:
                attrs['setid'] = setid

            card = ElementTree.SubElement(sections[section], 'card', attrs)
            card.text = name

        return ElementTree.tostring(root, encoding='unicode')


class CockatriceEncoder(Encoder):
    """Encoding class for the Cockatrice format.

    """
    def _encode(self, obj):
        root = ElementTree.Element('cockatrice_deck')
        sections = {}

        for name, attrs in obj:
            section = attrs.get('section', 'main')
            setid = attrs.get('setid', None)
            count = attrs['count']

            if section not in sections:
                sections[section] = ElementTree.SubElement(root, 'zone',
                                                           {'name': section})

            attrs = {'number': str(count), 'name': name}
            if setid:
                attrs['setid'] = setid

            ElementTree.SubElement(sections[section], 'card', attrs)

        return ElementTree.tostring(root, encoding='unicode')
