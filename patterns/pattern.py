from nltk import Tree

class pattern:

    _query_tree = None
    CONTEXT_OBJECT = 'OBJECT'
    CONTEXT_PROPERTY = 'PROPERTY'

    def __init__(self):
        pass

    def match(self, tree):
        """
        Hahahah!
        """
        if not isinstance(tree, Tree):
            raise AttributeError

        self._query_tree = tree

    def extract_answer(self, parts):
        raise NotImplementedError

    def search(self, parts):
        raise NotImplementedError

    def get_query_tree(self):
        return self._query_tree

