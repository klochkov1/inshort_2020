import random 

_alphabet = \
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-" 
    # this alphabet based on base64, but changed 2 last char
_alph_len = len(_alphabet)


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
    def __init__(self, str_len, flow_percent=5, reserved_words=[]):
        self.__word_len = str_len
        self.__used_str = list() # elements of list is tuple (word_id, word)
        self.__max_elem = _alph_len ** self.__word_len - 1
        self.__owerflow_count = self.__max_elem * flow_percent // 100
        self.__reserved = reserved_words
        self.add_word_list(self.__reserved)
    
    def add_word_list(self, word_list):
        for i in word_list:
            self.add_word_if_unused(i)

    @property
    def is_not_overflowed(self):
        return not self.is_overflowed

    @property
    def is_overflowed(self):
        return  len(self.__used_str) > self.__owerflow_count

    @property
    def is_empty(self):
        return len(self.__used_str) == 0

    @property
    def word_len(self):
        return self.__word_len

    @property
    def avaliable_len(self):
        return self.__max_elem - len(self.__used_str) + 1

    @property
    def __avaliable_len(self):
        return self.__max_elem - len(self.__used_str) + 1
    
    def get_random_word(self):
        if self.__avaliable_len <= 0:
            raise Exception("Words owerflow")
        pos = random.randrange(self.__avaliable_len) 
        # pos linked to position of free id. pos starts from 0
        # that mean if pos=4, but id 2,3 is already declared res id = 5
        words = self.__used_str
        words_len = len(words)
        res = ""
        if words_len == 0 or words[-1][0] < pos + words_len:  
            pos += words_len
            res = _get_word_from_id(pos, self.__word_len)
            words.append((pos, res))
        else:
            for i in range(words_len):
                # here pos is more close to id
                # we add 1 to pos to pass id which is already declared 
                if words[i][0] > pos:
                    res = _get_word_from_id(pos, self.__word_len)
                    words.insert(i, (pos, res))
                    break
                pos += 1
        return res

    def __is_exisist_and_position(self, word_id):
        """return (is_exist, position)"""
        words = self.__used_str
        if len(words) == 0 or words[0][0] > word_id:
            return (False, 0)
        elif word_id > words[-1][0]:
            return (False, len(words))
        start = 0
        end = len(words) - 1
        while end > start:
            mid = (end + start) // 2
            cur_id = words[mid][0]
            if cur_id == word_id:
                return (True, mid)
            elif cur_id > word_id:
                end = mid - 1
            else:
                start = mid + 1
        if words[start][0] == word_id:
            return (True, start)
        pos = start  if words[start][0] > word_id else start + 1
        return (False, pos) 

    def remove_word(self, word):
        word_id = _get_id(word, self.__word_len)
        is_exist, pos = self.__is_exisist_and_position(word_id)
        if is_exist:
            del self.__used_str[pos]
    
    def add_word_if_unused(self, word):
        word_id = _get_id(word, self.__word_len)
        is_exist, pos = self.__is_exisist_and_position(word_id)
        if not is_exist:
            self.__used_str.insert(pos, (word_id, word))
        return not is_exist
    
    def is_word_unused(self, word):
        word_id = _get_id(word, self.__word_len)
        is_exist= self.__is_exisist_and_position(word_id)[0]
        return not is_exist

    def __str__(self):
        res = ""
        res += f"words len = {self.__word_len}\n"
        res += f"Max elem = {self.__max_elem}\n"
        res += f"Owerflow count = {self.__owerflow_count}\n"
        res += f"Reversed = {self.__reserved}\n"
        res += f"Words = {self.__used_str}\n"
        return res

    def get_all_words(self):
        return [ i[1] for i in self.__used_str ]
   