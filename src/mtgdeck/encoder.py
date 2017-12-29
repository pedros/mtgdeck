"""Encoder implementations for mtgdeck."""

from .base.encoder import (TextEncoder, XMLEncoder)


class EncodeError(Exception):
    """Format encoding exception."""
    def __str__(self):
        return 'Could not determine encoding format: {}'.format(self.args)


class MagicOnlineEncoder(TextEncoder):
    """Encoding class for the simple text format.

    This is the format that MTGO outputs. Each line has the form 'quantity
    name'. An optional line containing the word 'Sideboard' indicates that
    subsequent entries are sideboard material.

    """
    def encode_entry(self, name, attrs):
        out = ''
        if attrs.get('section', False) == 'Sideboard':
            if not getattr(self, 'sideboard', False):
                setattr(self, 'sideboard', True)
                out = 'Sideboard\n'
        return out + '{} {}\n'.format(attrs['count'], name)


class MagicWorkstationEncoder(TextEncoder):
    """Encoding class for the Magic Workstation format.

    Each line has the form '[SB: ]quantity [SETID ]name', '[]' meaning optional
    fields.

    """
    def encode_entry(self, name, attrs):
        entries = []

        if 'section' in attrs:
            entries.append('SB:')

        entries.append(str(attrs['count']))

        if 'setid' in attrs:
            entries.append('[{}]'.format(attrs['setid']))

        entries.append('{}\n'.format(name))

        return ' '.join(entries)


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
