from abc import ABCMeta, abstractmethod
from io import StringIO
from xml.etree import ElementTree
from pyparsing import (Group, Keyword, OneOrMore, Optional, ParseException,
                       Word, cppStyleComment, empty, nestedExpr, nums,
                       restOfLine)


class MtgDeckDecodeError(Exception):
    def __str__(self):
        return 'Could not determine decoding format: {}'.format(self.args)


class MtgDeckDecoder(metaclass=ABCMeta):

    @abstractmethod
    def _decode(self, string):
        return []

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, string):
        src = string.replace('\r\n', '\n').replace('\r', '\n')
        return list(self._decode(src))


class MtgDeckAutoDecoder(MtgDeckDecoder):
    def _decode(self, string): pass

    def loads(self, string):
        exceptions = []
        for cls in MtgDeckDecoder.__subclasses__():
            if cls == self.__class__:
                continue
            try:
                return cls().loads(string)
            except (ParseException,
                    AssertionError,
                    ElementTree.ParseError) as e:
                exceptions.append(cls)
        raise MtgDeckDecodeError(exceptions)


class MtgDeckTextDecoder(MtgDeckDecoder):
    def __init__(self):
        self.Comment = cppStyleComment
        self.Section = Keyword('Sideboard')
        self.Count = Word(nums)
        self.Card = empty + restOfLine
        self.Entry = Group(self.Count + self.Card)
        self.Deck = OneOrMore(self.Comment |
                              self.Section |
                              self.Entry).ignore(self.Comment)

    def _decode(self, string):
        entries = self.Deck.parseString(string, parseAll=True)
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


class MtgDeckMagicWorkstationDecoder(MtgDeckDecoder):
    def __init__(self):
        self.Comment = cppStyleComment
        self.Section = Keyword('SB:')
        self.Count = Word(nums)
        self.Set = nestedExpr('[', ']')
        self.Card = empty + restOfLine
        self.Entry = Group(Optional(self.Section, None) +
                           self.Count +
                           Optional(self.Set, []) +
                           self.Card)
        self.Deck = OneOrMore(self.Comment | self.Entry).ignore(self.Comment)

    def _decode(self, string):
        entries = self.Deck.parseString(string)
        for entry in entries:
            section, count, setid, card = entry

            attrs = {'count': int(count)}

            if len(setid):
                attrs['setid'] = setid[0]
            if section:
                attrs['section'] = 'Sideboard'

            yield card, attrs


class MtgDeckOCTGNDecoder(MtgDeckDecoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert(tree.getroot().tag == 'deck')

        for section in tree.findall('section'):
            for entry in section.findall('card'):
                count = entry.attrib['qty']
                card = entry.text
                yield card, {'section': section.attrib['name'],
                             'count': int(count)}


class MtgDeckCockatriceDecoder(MtgDeckDecoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert(tree.getroot().tag == 'cockatrice_deck')

        for section in tree.findall('zone'):
            for entry in section.findall('card'):
                count = entry.attrib['number']
                card = entry.attrib['name']
                yield card, {'section': section.attrib['name'],
                             'count': int(count)}
