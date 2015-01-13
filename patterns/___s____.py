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

            object = Tree('NP', self.get_query_tree()[0][:-1])
            property = Tree('NP', self.get_query_tree()[1:])
            return [
                {'tree': property, 'context': 'PROPERTY'},
                {'tree': object, 'context': 'OBJECT'}
            ]


        except IndexError:
            return None


