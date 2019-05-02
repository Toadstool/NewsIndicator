from io import StringIO
from collections import OrderedDict

from mmap import mmap
import os
import struct
import sys
from accents import AccentsTable, Accents
import marisa_trie


NAME_FILENAME = '.pydic'
FORMS_HASH_FILENAME = 'forms.hash'
FORMS_RECNO_FILENAME = 'forms.recno'
FORMS_RECNO_INDEX_FILENAME = 'forms.recno.index'

class ConfigurationErrorException(Exception):
    pass

class PyDicId(object):
    """
    Dictionary lexem identifier. Build from sequential number (an id) and
    dictionary name concatenated with '@' sign, eg. '123@sjp'
    """
    SEPARATOR = '@'

    def __init__(self, ident=None, dict_name=None):
        if (type(ident) == str or type(ident) == str) and dict_name is None:
            self.id, self.dict = self.parse_text_ident(ident)
        elif ident is not None and dict_name is not None:
            self.id = int(ident)
            self.dict = str(dict_name)
        else:
            raise ValueError('Cannot create valid PyDic ID')

    def parse_text_ident(self, text_ident):
        ident, dictionary = str(text_ident).split(PyDicId.SEPARATOR)
        return (int(ident), dictionary)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(str(self)))

    def __str__(self):
        return "%d%s%s" % (self.id, PyDicId.SEPARATOR, self.dict)

    def __unicode__(self):
        return "%d%s%s" % (self.id, PyDicId.SEPARATOR, self.dict)

    def __eq__(self, other):
        if type(other) == self.__class__:
            return self.dict == other.dict and self.id == other.id
        elif type(other) == str or type(other) == str:
            other = PyDicId(other)
            return self.dict == other.dict and self.id == other.id
        else:
            raise NotImplementedError()

    def __hash__(self):
        return hash(str(self))


def require_valid_pydic_id(method):
    def decorated(self, pydic_id):
        if type(pydic_id) == PyDicId:
            if not pydic_id.dict == self.name:
                raise ValueError('PyDic ID from different dictionary')
        elif type(pydic_id) in (str, str):
            pydic_id = PyDicId(pydic_id)
        elif type(pydic_id) == int:
            pydic_id = PyDicId(pydic_id, self.name)
        else:
            pydic_id = PyDicId(pydic_id)
        return method(self, pydic_id)

    decorated.__doc__ = method.__doc__
    decorated.__repr__ = method.__repr__
    return decorated


class PyDic(object):
    """
    Abstraction layer for accessing single dictionary
    """
    RECNO_INDEX_FMT = '<L'
    MARISA_HASH_FMT = '<L'
    DIR_EXTENSION = 'pydic'
    INTERNAL_DELIMITER = ':'

    def __init__(self, path):
        self.path = path
        if os.path.isdir(self.get_path()):
            self.read_pydic_index(self.get_path())
        elif os.path.isfile(self.path):
            self.make_memory_pydic_index(self.get_path())
        else:
            raise RuntimeError("cd")
        self.accents = Accents()

        self.memory_recno = ''

    def __iter__(self):
        return map(lambda i: PyDicId(i, self.name), range(1, len(self) + 1))

    def __len__(self):
        return self.recno_size

    def is_inmemory(self):
        """
        Checks if dictionary is in in-memory only mode. It is needed by other modules
        willing to write some intermediate file structures to pydic folder.
        """
        return os.path.isfile(self.path)

    def get_path(self, join_with=None):

        if join_with:
            return os.path.join(self.path, join_with)
        else:
            return self.path

    def id(self, form):
        """
        Returns a list of PyDicId that match a given word form

        :param form: word form
        :type form: unicode
        :return: list of PyDicId or empty list
        """
        try:
            return [PyDicId(x[0], self.name) for x in self.hash[form.lower()]]
        except KeyError:
            return []

    def a_id(self, form):
        """
        Accents agnostic version of method ``id()``

        :param form: form
        :type form: unicode
        :return: list of PyDicId or empty list
        """
        ids = set(self.id(form))
        for w in self.accents.make_accents(form):
            ids.update(self.id(w))
        return list(ids)

    @require_valid_pydic_id
    def id_forms(self, pydic_id):
        """
        Returns list of forms for a given PyDicId

        :param pydic_id: PyDicId or string id
        :type pydic_id: PyDicId, string
        :return: list of unicode strings or empty list
        """
        if self.is_inmemory():
            try:
                offset = self.recno_index[pydic_id.id-1]
            except IndexError:
                return []
        else:
            try:
                self.recno_index.seek(
                    (pydic_id.id - 1) * struct.calcsize(PyDic.RECNO_INDEX_FMT))
                offset = struct.unpack(PyDic.RECNO_INDEX_FMT, self.recno_index.read(
                    struct.calcsize(PyDic.RECNO_INDEX_FMT)))[0]
            except ValueError:
                return []

        self.recno.seek(offset)
        return self.__decode_form(self.recno.readline().rstrip())


    def word_forms(self, form):
        """
        Returns list of list of forms for a given form

        :param form: word form
        :type form: unicode
        :return: list of lists of unicode strings or empty list
        """

        return [self.id_forms(x) for x in self.id(form)]


    def a_word_forms(self, form, mapping=AccentsTable.PL):
        """
        Accent agnostic version of word_forms method.

        :param form: word form
        :type form: unicode
        :return: list of lists of unicode strings or empty list
        """

        return [self.id_forms(x) for x in self.a_id(form)]


    def __decode_form(self, string):
        """
        Internal function to decode string format stored in Recno

        :param string:
        :return:
        """
        bits = string.split(PyDic.INTERNAL_DELIMITER)
        return [bits[0] + x for x in bits[1:]]

    @require_valid_pydic_id
    def id_base(self, pydic_id):
        """
        Returns a base form of word given as PyDicId

        :param pydic_id: PyDicId
        :type pydic_id: PyDicId, string
        :return: unicode string or ``None``
        """

        try:
            return self.id_forms(pydic_id)[0]
        except IndexError:
            return None

    def word_base(self, form):
        """
        Returns a list of base forms of form

        :param form: word form
        :type form: unicode string
        :return: list of unicode strings or empty list
        """
        return list(set([self.id_base(x) for x in self.id(form)]))


    def a_word_base(self, form):
        """
        Accents agnostic version of ``word_base()`` method

        :param form: word form
        :type form: unicode string
        :return: list of unicode strings or empty list
        """
        return list(set([self.id_base(x) for x in self.a_id(form)]))


    def read_pydic_index(self, dic_path):
        self.dic_path = dic_path

        self.name = open(self.get_path(NAME_FILENAME),encoding="utf-8").read().strip()
        self.hash = marisa_trie.RecordTrie(PyDic.MARISA_HASH_FMT)
        self.hash.load(self.get_path(FORMS_HASH_FILENAME))

        recno_file = open(self.get_path(FORMS_RECNO_FILENAME), 'r+b',encoding="utf-8")
        recno_index_file = open(self.get_path(FORMS_RECNO_INDEX_FILENAME), 'r+b',encoding="utf-8")
        self.recno = mmap(recno_file.fileno(), 0)
        self.recno_index = mmap(recno_index_file.fileno(), 0)
        self.recno_size = self.recno_index.size() / struct.calcsize(
            PyDic.RECNO_INDEX_FMT)


    def make_memory_pydic_index(self, from_source, name=None, delimiter=',',
                                verbose=False):
        self.hash, self.recno, self.recno_index = PyDic.make_pydic_index(
            from_source=open(from_source,encoding="utf-8"),
            to_path=None,
            name=name,
            delimiter=delimiter,
            verbose=verbose)

        self.name = from_source
        self.recno_size = len(self.recno_index)

    @staticmethod
    def make_pydic_index(from_source, to_path, name, delimiter=',', verbose=False):


        if to_path is not None and os.path.exists(os.path.join(to_path, NAME_FILENAME)):
            raise ConfigurationErrorException(
                'Cowardly refusing to create dictionary in non empty directory')

        if to_path is not None and not os.path.exists(to_path):
            os.makedirs(to_path)

        if to_path is not None:
            name_file = open(os.path.join(to_path, NAME_FILENAME), 'w+',encoding="utf-8")
            name_file.write(name.encode('utf-8') + '\n')
            name_file.close()

        recno = StringIO()
        recno_index = []
        if to_path is not None:
            recno = open(os.path.join(to_path, FORMS_RECNO_FILENAME), 'w+b',encoding="utf-8")
            recno_index = open(os.path.join(to_path, FORMS_RECNO_INDEX_FILENAME), 'w+b',encoding="utf-8")

        def get_next_form(recno, recno_index):

            file_offset = 0
            recno_counter = 0

            for line in from_source:               
                bits = line.split(delimiter)
                bits = [x.strip() for x in bits]
                bits = [x for x in bits if x]
                if bits:
                    recno_counter += 1

                    bits = list(OrderedDict.fromkeys(bits).keys()) # stable unique
                    bits_prefixed = PyDic.common_prefix(bits)

                    bits_str = (PyDic.INTERNAL_DELIMITER.join(bits_prefixed)) + '\n'

                    recno.write(bits_str)

                    if to_path is None:
                        recno_index.append(file_offset)
                    else:

                        recno_index.write(
                            struct.pack(PyDic.RECNO_INDEX_FMT, file_offset))

                    if verbose:
                        print("[", recno_counter, "]", bits[0], file=sys.stderr)

                    for bit in bits:
                        yield bit.lower(), (recno_counter, )
                    file_offset += len(bits_str)
            #raise StopIteration

        forms_index = marisa_trie.RecordTrie(PyDic.MARISA_HASH_FMT,
                                             get_next_form(recno, recno_index
                                                           ))
        if to_path is not None:
            forms_index.save(os.path.join(to_path, FORMS_HASH_FILENAME))

        return forms_index, recno, recno_index

    @staticmethod
    def common_prefix(word_list):
        """
        For a list of words produces a list of [optimal prefix, suffix1, suffix2...]
        :param word_list:
        :return:
        """
        i = min([len(x) for x in word_list])
        while i > 0:
            lst = [x[0:i] for x in word_list]
            # http://stackoverflow.com/questions/3844801
            # Fastest checking if lst has the same values
            if (not lst or lst.count(lst[0]) == len(lst)):
                break
            i -= 1
        return [word_list[0][0:i]] + [x[i:] for x in word_list]





if __name__ == '__main__':    
    sjp = PyDic('sjp_clean.txt')
    print(sjp.word_base(u'telefonował'))
    print(sjp.a_word_base(u'wariatkowo'))
    print(sjp.word_base(u'takiegoSlowaNiema'))