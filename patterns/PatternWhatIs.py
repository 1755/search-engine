from nltk import ParentedTree
from search_engine.components.data_base import DataBase
from search_engine.patterns.pattern import Pattern


class PatternWhatIs(Pattern):

    def __init__(self):
        self._parts = []
        self._keyword = 'what'
        Pattern.__init__(self)

    def match(self, *args, **kwargs):
        Pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != "ROOT":
                raise IndexError

            if self.get_query_tree()[0].label() != "SBARQ":
                raise IndexError

            if self.get_query_tree()[0][0].label() != "WHNP":
                raise IndexError

            if self.get_query_tree()[0][0][0].label() != "WP":
                raise IndexError

            if self.get_query_tree()[0][0][0][0].lower() != self._keyword:
                raise IndexError

            if self.get_query_tree()[0][1].label() != "SQ":
                raise IndexError

            if len(self.get_query_tree()[0][1]) < 2:
                raise IndexError

            part = Pattern.Part()
            part.object = ParentedTree.fromstring(str(self.get_query_tree()[0][1][1]))
            self._parts.append(part)

            return self._parts

        except IndexError:
            return []

    def search(self, part):
        query = " ".join(part.object.leaves())
        return DataBase().search(query)

    def extract_answer(self, property_tree, object_from_database):
        return [object_from_database]