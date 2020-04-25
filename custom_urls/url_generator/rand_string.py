from fixed_string import RandFixedLenStrStorage as rand_str

class StringGenerator:
    def __init__(self, def_len=4, flow_percent=5, reserve_word_list=[]):
        self.__def_len = def_len
        self.__flow_percent = flow_percent
        self.__generator_list = list()
        self.add_word_list(reserve_word_list)

    def add_word_list(self, word_list):
        word_dict = {}
        for i in word_list:
            word_dict.setdefault(len(i), []).append(i)
        for i in word_dict:
            gen = self.__get_generator_with_len(i)
            gen.add_word_list(word_dict[i])

    def __get_generator_with_len(self, word_len):
        layers = self.__generator_list
        if len(layers) == 0 or word_len > layers[-1].word_len:
            layer = rand_str(word_len, self.__flow_percent)
            layers.append(layer)
            return layer
        else:
            for i in range(len(layers)):
                cur_layer = layers[i]
                if cur_layer.word_len == word_len:
                    return cur_layer
                elif cur_layer.word_len > word_len:
                    layer = rand_str(word_len, self.__flow_percent)
                    layers.insert(i, layer)
                    return layer
        
    def get_random_word(self):
        cur_len = self.__def_len
        cur_gen = self.__get_generator_with_len(cur_len)
        while cur_gen.is_overflowed:
            cur_len += 1
            cur_gen = self.__get_generator_with_len(cur_len)
        return cur_gen.get_random_word()

    def get_random_word_with_len(self, word_len):
        cur_gen = self.__get_generator_with_len(word_len)
        return cur_gen.get_random_word()

    def get_all_words(self):
        res = []
        for i in self.__generator_list:
            res.extend(i.get_all_words())
        return res

    def add_word_if_unused(self, word):
        cur_gen = self.__get_generator_with_len(len(word))
        return cur_gen.add_word_if_unused(word)

    def is_word_unused(self, word):
        cur_gen = self.__get_generator_with_len(len(word))
        return cur_gen.is_word_unused(word)
    
    def remove_word(self, word):
        cur_gen = self.__get_generator_with_len(len(word))
        return cur_gen.remove_word(word)

    def __str__(self):
        res = ""
        res += f"def len = {self.__def_len}\n"
        res += f"flow_ps = {self.__flow_percent}\n"
        res += "List -------------------------------------------------------------------\n"
        for i in self.__generator_list:
            res += f"{i}\n"
            res += "-------------------------------------------------------------------\n"
        return res
