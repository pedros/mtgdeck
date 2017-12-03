from abc import ABCMeta, abstractmethod
from xml.etree import ElementTree


class MtgDeckEncodeError(object):
    pass


class MtgDeckEncoder(metaclass=ABCMeta):
    """Abstract base class for encoders.

    Only one method must be implemented: ``_encode``"""

    @abstractmethod
    def _encode(self, obj): pass

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
    """Encoding class for text formats.

    This is the format that MTGO outputs. Each line has the form 'quantity
    name'. An optional line containing the word 'Sideboard' indicates that
    subsequent entries are sideboard material.

    Examples
    --------
    >>> import mtgdeck.encoder
    >>> mtgdeck.encoder.MtgDeckTextEncoder()
    <mtgdeck.encoder.MtgDeckTextEncoder...>
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
    def _encode(self, obj):
        out = ''
        for section, name, setid, count in self._scatter(obj):
            if setid:
                out += '{}: {} [{}] {}\n'.format(section, count, setid, name)
            else:
                out += '{}: {} {}\n'.format(section, count, name)
        return out


class MtgDeckOCTGNEncoder(MtgDeckEncoder):
    def _encode(self, string): raise NotImplementedError(self)


class MtgDeckCockatriceEncoder(MtgDeckEncoder):
    def _encode(self, string): raise NotImplementedError(self)
