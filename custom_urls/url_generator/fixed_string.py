import random 

_alphabet = \
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" 
    # "-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz" 
    # this alphabet based on base64, but changed 2 last char
_alph_len = len(_alphabet)

def is_walid_url(word):
    for i in word:
        if i not in _alphabet:
            return False
    return True

def _get_word_from_id(num, size):
    res = ""
    n = num
    for i in range(size):
        res = _alphabet[ n % _alph_len ] + res
        n //= _alph_len
    return res

def _get_id(word, size):
    if size != len(word):
        raise Exception("Word has wrong size")
    res = 0
    for i in word:
        res *= _alph_len
        pos = _alphabet.find(i)
        if pos < 0:
            raise Exception(f"Letter {i} out of alphabet")
        else:
            res += pos
    return res

class RandFixedLenStrStorage:
    def __init__(self, str_len, word_list, flow_percent=5):
        self.__word_list = sorted(list(word_list))
        self.__word_len = str_len
        self.__max_elem = _alph_len ** self.__word_len - 1
        self.__owerflow_count = self.__max_elem * flow_percent // 100

    @property
    def is_not_overflowed(self):
        return not self.is_overflowed

    @property
    def is_overflowed(self):
        return  self.count > self.__owerflow_count

    @property
    def is_empty(self):
        return self.count == 0

    @property
    def count(self):
        return len(self.__word_list)

    @property
    def word_len(self):
        return self.__word_len

    def get_random_word(self):
        #returns id
        words = self.__word_list
        words_len = len(words)
        avaliable_len = self.__max_elem - words_len + 1
        if avaliable_len <= 0:
            raise Exception("Words owerflow")
        pos = random.randrange(avaliable_len) 
        # pos linked to position of free id. pos starts from 0
        # that mean if pos=4, but id 2,3 is already declared res id = 5
        res = ""
        last_url = _get_word_from_id(pos + words_len, self.__word_len)
        if words_len == 0 or words[-1] < last_url:
            res = last_url
        else:
            cur_url = _get_word_from_id(pos, self.__word_len)
            for i in range(words_len):
                # here pos is more close to id
                # we add 1 to pos to pass id which is already declared 
                if words[i] > cur_url:
                    cur_url = _get_word_from_id(pos, self.__word_len)
                    if words[i] > cur_url:
                        res = cur_url
                        break
                pos += 1
        return res

