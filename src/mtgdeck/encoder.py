"""Encoder implementations for mtgdeck."""

from .base.encoder import (EncodeError, Encoder, XMLEncoder)


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


class OCTGNEncoder(XMLEncoder):
    """Encoding class for the OCTGN Deck Creator format."""
    root = 'deck'
    section = 'section'
    section_name = 'Main'
    count = 'qty'

    def set_content(self, card, name):
        card.text = name


class CockatriceEncoder(XMLEncoder):
    """Encoding class for the Cockatrice format."""
    root = 'cockatrice_deck'
    section = 'zone'
    section_name = 'main'
    count = 'number'

    def set_content(self, card, name):
        card.attrib['name'] = name
