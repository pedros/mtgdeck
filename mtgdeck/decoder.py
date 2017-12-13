from abc import ABCMeta, abstractmethod
from io import StringIO
from xml.etree import ElementTree
from pyparsing import (Group, Keyword, OneOrMore, Optional, ParseException,
                       Word, cppStyleComment, empty, nestedExpr, nums,
                       restOfLine)


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
        for cls in Decoder.__subclasses__():
            if cls == self.__class__:
                continue
            try:
                return cls().loads(string)
            except (ParseException,
                    AssertionError,
                    ElementTree.ParseError) as _:
                exceptions.append(cls)
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


class OCTGNDecoder(Decoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert tree.getroot().tag == 'deck'

        for section in tree.findall('section'):
            for entry in section.findall('card'):
                count = entry.attrib['qty']
                card = entry.text
                yield card, {'section': section.attrib['name'],
                             'count': int(count)}


class CockatriceDecoder(Decoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert tree.getroot().tag == 'cockatrice_deck'

        for section in tree.findall('zone'):
            for entry in section.findall('card'):
                count = entry.attrib['number']
                card = entry.attrib['name']
                yield card, {'section': section.attrib['name'],
                             'count': int(count)}
