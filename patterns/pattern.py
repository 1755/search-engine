from nltk import Tree
from search_engine.searchers.freebase import Freebase


class pattern:

    _query_tree = None
    _freebase = Freebase()
    CONTEXT_OBJECT = "OBJECT"

    def __init__(self):
        pass

    def match(self, *args, **kwargs):
        if 'query_tree' not in kwargs:
            raise AttributeError
        if not isinstance(kwargs['query_tree'], Tree):
            raise AttributeError

        self._query_tree = kwargs['query_tree']
        pass

    def extract_answer(self, parts):
        raise NotImplementedError

    def search(self, parts):
        raise NotImplementedError

    def get_query_tree(self):
        return self._query_tree
