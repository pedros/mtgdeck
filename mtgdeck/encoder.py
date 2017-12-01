from abc import ABCMeta, abstractmethod


class MtgDeckEncodeError(object):
    pass


class MtgDeckBaseEncoder(metaclass=ABCMeta):

    @abstractmethod
    def _encode(self, obj): pass

    def _scatter(self, obj):
        for section, cards in obj.items():
            for name, attrs in cards.items():
                for setid, count in attrs.items():
                    yield (count, name, section, setid)

    def dump(self, obj, fp):
        fp.write(self.dumps(obj))

    def dumps(self, obj):
        return self._encode(obj)


class MtgDeckTextEncoder(MtgDeckBaseEncoder):
    def _encode(self, obj):
        out = ''
        for section, cards in obj.items():
            # if section == 'side':
            out += '{}\n'.format(section)
            for name, attrs in cards.items():
                for setid, count in attrs.items():
                    out += '{} {}\n'.format(count, name)
        return out


class MtgDeckMagicWorkstationEncoder(MtgDeckBaseEncoder):
    def _encode(self, obj):
        out = ''
        for count, name, section, setid in self._scatter(obj):
            if setid:
                out += '{}: {} [{}] {}\n'.format(section, count, setid, name)
            else:
                out += '{}: {} {}\n'.format(section, count, name)
        return out


class MtgDeckOCTGNEncoder(MtgDeckBaseEncoder):
    def _encode(self, string): raise NotImplementedError


class MtgDeckCockatriceEncoder(MtgDeckBaseEncoder):
    def _encode(self, string): raise NotImplementedError
