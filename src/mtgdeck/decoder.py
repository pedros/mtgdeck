from abc import ABCMeta, abstractmethod
from io import StringIO
from pyparsing import (Group, Keyword, OneOrMore, Optional, Word,
                       cppStyleComment, empty, nestedExpr, nums, restOfLine)


class DecodeError(Exception):
    def __str__(self):
        return 'Could not determine decoding format: {}'.format(self.args)


class Decoder(metaclass=ABCMeta):

    @abstractmethod
    def _decode(self, string):
        return []

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, string):
        src = string.replace('\r\n', '\n').replace('\r', '\n')
        return list(self._decode(src))


class AutoDecoder(Decoder):
    def _decode(self, string):
        pass

    def loads(self, string):
        exceptions = []
        for cls in (TextDecoder, MagicWorkstationDecoder,
                    OCTGNDecoder, CockatriceDecoder):
            try:
                return cls().loads(string)
            except Exception as _:
                exceptions.append((cls, _))
        raise DecodeError(exceptions)


class TextDecoder(Decoder):
    def __init__(self):
        self.comment = cppStyleComment
        self.section = Keyword('Sideboard')
        self.count = Word(nums)
        self.card = empty + restOfLine
        self.entry = Group(self.count + self.card)
        self.deck = OneOrMore(self.comment |
                              self.section |
                              self.entry).ignore(self.comment)

    def _decode(self, string):
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
    def __init__(self):
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
    def __init__(self):
        import importlib.util
        if importlib.util.find_spec('defusedxml'):
            from defusedxml.ElementTree import parse as parser
        else:
            from xml.etree.ElementTree import parse as parser
        self.parser = parser

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
    def count(self):
        """Quantity (ie: qty, number) tag for the XML format."""

    def _decode(self, string):
        fp = StringIO(string)
        tree = self.parser(fp)

        if tree.getroot().tag != self.root:
            raise KeyError('Missing a "{}" tag', self.root)

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
    root = 'deck'
    section = 'section'
    count = 'qty'


class CockatriceDecoder(XMLDecoder):
    root = 'cockatrice_deck'
    section = 'zone'
    count = 'number'
