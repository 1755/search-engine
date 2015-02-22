from nltk import Tree
from search_engine.patterns import ____of____
from search_engine.patterns.pattern import pattern


class ___s____(____of____):
    def match(self, *args, **kwargs):
        pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != "NP":
                raise IndexError

            if self.get_query_tree()[0].label() != "NP":
                raise IndexError

            if self.get_query_tree()[0][-1].label() != "POS":
                raise IndexError

            self._object_part = Tree('NP', self.get_query_tree()[0][:-1])
            self._property_part = Tree('NP', self.get_query_tree()[1:])
            return [
                {'tree': self._property_part, 'context': 'PROPERTY'},
                {'tree': self._object_part, 'context': 'OBJECT'}
            ]


        except IndexError:
            return None


