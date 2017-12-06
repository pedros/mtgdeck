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

    def _gather(self, entries):
        deck = {}

        for section, card, setid, count in entries:
            if section not in deck:
                deck[section] = {}
            if card not in deck[section]:
                deck[section][card] = {}
            if setid not in deck[section][card]:
                deck[section][card][setid] = count
            else:
                deck[section][card][setid] += count

        return deck

    def load(self, fp):
        return self.loads(fp.read())

    def loads(self, string):
        src = string.replace('\r\n', '\n').replace('\r', '\n')
        return self._gather(self._decode(src))


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
        section = 'mainboard'
        for entry in entries:
            try:
                count, card = entry
                yield(section, card, None, int(count))
            except ValueError as _:
                section = entry
                continue


class MtgDeckMagicWorkstationDecoder(MtgDeckDecoder):
    def __init__(self):
        self.Comment = cppStyleComment
        self.Section = Keyword('SB:')
        self.Count = Word(nums)
        self.Set = nestedExpr('[', ']')
        self.Card = empty + restOfLine
        self.Entry = Group(Optional(self.Section) +
                           self.Count +
                           Optional(self.Set) +
                           self.Card)
        self.Deck = OneOrMore(self.Comment | self.Entry).ignore(self.Comment)

    def _decode(self, string):
        entries = self.Deck.parseString(string, parseAll=True)
        for entry in entries:
            count = 0
            card = ''
            section = 'mainboard'
            setid = []

            if entry[0] == 'SB:':
                section = 'sideboard'
            else:
                section = 'mainboard'

            n = len(entry)

            if n == 2:
                count, card = entry
            elif n == 3:
                if section == 'sideboard':
                    _, count, card = entry
                else:
                    count, setid, card = entry
            elif n == 4:
                _, count, setid, card = entry

            yield (section, card,
                   setid[0] if len(setid) else None,
                   int(count))


class MtgDeckOCTGNDecoder(MtgDeckDecoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert(tree.getroot().tag == 'deck')

        for section in tree.findall('section'):
            for entry in section.findall('card'):
                count = entry.attrib['qty']
                card = entry.text
                yield (section.attrib['name'], card, None, int(count))


class MtgDeckCockatriceDecoder(MtgDeckDecoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert(tree.getroot().tag == 'cockatrice_deck')

        for section in tree.findall('zone'):
            for entry in section.findall('card'):
                count = entry.attrib['number']
                card = entry.attrib['name']
                yield (section.attrib['name'], card, None, int(count))
