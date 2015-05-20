from nltk import ParentedTree, Tree
from patterns.pattern import Pattern


class PatternWhenWasObjectAction(Pattern):
    def __init__(self):
        super(PatternWhenWasObjectAction, self).__init__()
        self._parts = []

    def match(self, tree):
        try:
            if tree.label() != 'ROOT':
                raise IndexError
            if tree[0].label() != 'SBARQ':
                raise IndexError
            if tree[0][0][0].label() != 'WRB':
                raise IndexError
            if tree[0][0][0][0].lower() != 'when':
                raise IndexError
            if tree[0][1].label() != 'SQ':
                raise IndexError
            if tree[0][1][0].label() != 'VBD':
                raise IndexError
            if tree[0][1][1].label() != 'NP':
                raise IndexError
            if tree[0][1][2].label() != 'VP':
                raise IndexError

            part = Pattern.Part()
            part.object = ParentedTree.fromstring(str(tree[0][1][1]))
            part.property = ParentedTree.fromstring(str(Tree('VP', [
                Tree.fromstring(str(tree[0][0][0])),
                Tree.fromstring(str(tree[0][1][0])),
                Tree.fromstring(str(tree[0][1][2]))
            ])))

            return [part]
        except IndexError:
            return []

    def extract_answer(self, property_tree, object_from_database):
        return None

