from io import StringIO
from xml.etree import ElementTree
from pyparsing import (Word, nums, restOfLine, Group, empty,
                       OneOrMore, ZeroOrMore, Optional,
                       cppStyleComment, nestedExpr, CaselessKeyword,
                       ParseException)


class MtgDeckDecodeError(ParseException):
    def __str__(self):
        return 'Could not determine encoding format: {}'.format(self.args)


class MtgDeckAutoDecoder(object):
    @staticmethod
    def _loads(string):
        exceptions = []
        for cls in MtgDeckAutoDecoder.__subclasses__():
            try:
                return cls().loads(string)
            except (ParseException, AssertionError) as e:
                exceptions.append(cls)
        raise MtgDeckDecodeError(exceptions)

    def load(self, fp):
        string = fp.read()
        return self.loads(string)

    def loads(self, string):
        src = string.replace('\r\n', '\n').replace('\r', '\n')
        return self._gather(map(self._format, self._decode(src)))

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

    def _format(self, entry):
        count, card, section, *setid = entry
        return section, card, setid[0] if len(setid) else None, int(count)

    def _decode(self, src):
        raise NotImplementedError('This method must be implemented')


class MtgDeckTextDecoder(MtgDeckAutoDecoder):
    Comment = cppStyleComment
    Section = (CaselessKeyword('sideboard') |
               CaselessKeyword('mainboard') +
               Optional(':'))
    Count = Word(nums)
    Card = empty + restOfLine
    Entry = Group(Count + Card)
    Deck = OneOrMore(Comment | Section | Entry).ignore(Comment)

    def _decode(self, string):
        entries = self.Deck.parseString(string)
        section = 'mainboard'
        for entry in entries:
            try:
                count, card = entry
            except ValueError as _:
                section = entry
            finally:
                yield (count, card, section)


class MtgDeckMagicWorkstationDecoder(MtgDeckAutoDecoder):
    Comment = cppStyleComment
    Section = CaselessKeyword('sb:')
    Count = Word(nums)
    Set = nestedExpr('[', ']')
    Card = empty + restOfLine
    Entry = Group(ZeroOrMore(Section) + Count + Optional(Set) + Card)
    Deck = OneOrMore(Comment | Entry).ignore(Comment)

    def _decode(self, string):
        entries = self.Deck.parseString(string)
        for entry in entries:
            count = 0
            card = ''
            section = 'mainboard'
            setid = []

            if entry[0] == 'sb:':
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

            yield (count, card, section,
                   setid[0] if len(setid) else None)


class MtgDeckOCTGNDecoder(MtgDeckAutoDecoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert(tree.getroot().tag == 'deck')

        for section in tree.findall('section'):
            for entry in section.findall('card'):
                count = entry.attrib['qty']
                card = entry.text
                yield (count, card, section.attrib['name'], None)


class MtgDeckCockatriceDecoder(MtgDeckAutoDecoder):
    def _decode(self, string):
        fp = StringIO(string)
        tree = ElementTree.parse(fp)

        assert(tree.getroot().tag == 'cockatrice_deck')

        for section in tree.findall('zone'):
            for entry in section.findall('card'):
                count = entry.attrib['number']
                card = entry.attrib['name']
                yield (count, card, section.attrib['name'], None)
