from abc import ABCMeta, abstractmethod
from xml.etree import ElementTree


class MtgDeckEncodeError(Exception):
    def __str__(self):
        return 'Could not determine encoding format: {}'.format(self.args)


class MtgDeckEncoder(metaclass=ABCMeta):
    """Abstract base class for encoders.

    Only one method must be implemented: ``_encode``

    """

    @abstractmethod
    def _encode(self, obj):
        return ''

    def _scatter(self, obj):
        for section, cards in obj.items():
            for name, attrs in cards.items():
                for setid, count in attrs.items():
                    yield (section, name, setid, count)

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj):
        return self._encode(obj)


class MtgDeckTextEncoder(MtgDeckEncoder):
    """Encoding class for the simple text format.

    This is the format that MTGO outputs. Each line has the form 'quantity
    name'. An optional line containing the word 'Sideboard' indicates that
    subsequent entries are sideboard material.

    """

    def _encode(self, obj):
        out = ''
        for section, cards in obj.items():
            # if section == 'side':
            out += '{}\n'.format(section)
            for name, attrs in cards.items():
                for setid, count in attrs.items():
                    out += '{} {}\n'.format(count, name)
        return out


class MtgDeckMagicWorkstationEncoder(MtgDeckEncoder):
    """Encoding class for the Magic Workstation format.

    Each line has the form '[SB: ]quantity [SETID ]name', '[]' meaning optional
    fields.

    """
    def _encode(self, obj):
        out = ''
        for section, name, setid, count in self._scatter(obj):
            if setid:
                out += '{}: {} [{}] {}\n'.format(section, count, setid, name)
            else:
                out += '{}: {} {}\n'.format(section, count, name)
        return out


class MtgDeckOCTGNEncoder(MtgDeckEncoder):
    """Encoding class for the OCTGN Deck Creator format.

    """
    def _encode(self, obj):
        root = ElementTree.Element('deck')
        sections = {}
        for section, name, setid, count in self._scatter(obj):

            if section not in sections:
                sections[section] = ElementTree.SubElement(root, 'section',
                                                           {'name': section})

            card = ElementTree.SubElement(sections[section], 'card',
                                          {'qty': str(count),
                                           'name': name})

            if setid:
                ElementTree.SubElement(card, 'property',
                                       {'name': 'setid', 'value': setid})

        return ElementTree.tostring(root, encoding='unicode')


class MtgDeckCockatriceEncoder(MtgDeckEncoder):
    """Encoding class for the Cockatrice format.

    """
    def _encode(self, obj):
        root = ElementTree.Element('cockatrice')
        sections = {}
        for section, name, setid, count in self._scatter(obj):

            if section not in sections:
                sections[section] = ElementTree.SubElement(root, 'zone',
                                                           {'name': section})

            ElementTree.SubElement(sections[section], 'card',
                                   {'number': str(count),
                                    'name': name})

        return ElementTree.tostring(root, encoding='unicode')
