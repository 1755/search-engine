from nltk import Tree
from search_engine.patterns.pattern import pattern

__author__ = 'egres'


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