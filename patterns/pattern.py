from nltk import ParentedTree
from components.data_base import DataBase


class Pattern(object):

    class Part(object):
        def __init__(self):
            self.object = None
            self.property = None


    _query_tree = None
    CONTEXT_OBJECT = 'OBJECT'
    CONTEXT_PROPERTY = 'PROPERTY'
    CONTEXT_VERB = 'VERB'
    CONTEXT_IN = 'IN'


    def match(self, tree):
        if not isinstance(tree, ParentedTree):
            raise AttributeError

        self._query_tree = ParentedTree.fromstring(str(tree))

    def extract_answer(self, property_tree, object_from_database):
        raise NotImplementedError

    def search(self, part):
        query = " ".join(part.object.leaves())
        return DataBase().search(query)

    def get_query_tree(self):
        return self._query_tree

