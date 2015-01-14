# coding=utf-8
from nltk import Tree
from search_engine.patterns.pattern import pattern

__author__ = 'egres'

# @todo: разобраться как производить apply.
#        Можно спросить the difference, а можно the distance
#        И скорее всего эти два случая будут обрабатываться по-разному
class ____between_____and____(pattern):
    def match(self, *args, **kwargs):
        pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != "NP":
                raise IndexError

            if len(self.get_query_tree()) != 2:
                raise IndexError

            if self.get_query_tree()[0].label() != "NP":
                raise IndexError

            if self.get_query_tree()[1].label() != "PP":
                raise IndexError

            if self.get_query_tree()[1][0].label() != "IN":
                raise IndexError

            if self.get_query_tree()[1][0][0].lower() != "between":
                raise IndexError

            if self.get_query_tree()[1][1].label() != "NP":
                raise IndexError

            cc_index = -1
            nodes = self.get_query_tree()[1][1]
            for node in nodes:
                if node.label() == "CC":
                    cc_index = nodes.index(node)
                    break

            if cc_index < 0:
                raise IndexError

            object_a = Tree('NP', nodes[0:cc_index])
            object_b = Tree('NP', nodes[cc_index+1:])
            prop = self.get_query_tree()[0]

            return [
                {'tree': prop, 'context': 'PROPERTY'},
                {'tree': object_a, 'context': 'OBJECT_A'},
                {'tree': object_b, 'context': 'OBJECT_B'}
            ]

        except IndexError:
            return None

    def search(self, parts):
        if parts is None:
            return None

        if len(parts) != 3:
            return None

        for part in parts:
            if 'tree' not in part:
                return None

        for part in parts:
            if part['context'] == 'PROPERTY':
                continue

            result = self._freebase.search(" ".join(part['tree'].leaves()))
            if result is None:
                return None

            part['data'] = self._freebase.get_topic(result['mid'])
            if part['data'] is None:
                return None

        return "some result"

    def apply_data(self, parts):
        object_a_part = None
        object_b_part = None
        property_part = None
        for part in parts:
            if part['context'] == 'PROPERTY':
                property_part = part

            if part['context'] == 'OBJECT_A':
                object_a_part = part

            if part['context'] == 'OBJECT_B':
                object_b_part = part

        if object_a_part is None:
            return None

        if 'data' not in object_a_part:
            return None

        if object_b_part is None:
            return None

        if 'data' not in object_b_part:
            return None

        if object_a_part['data'] is None:
            return None

        if object_b_part['data'] is None:
            return None


        # print(property_part['tree'])
        # print(object_a_part['tree'])
        # print(object_b_part['tree'])
        print(self.__class__.__name__ + ".apply_data() not implemented yet")
        return None

