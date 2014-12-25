from nltk.tree import Tree
from searchers.object import Object

class WIPOO:
    _tree = None
    _property = None
    _object = None

    def __init__(self):
        pass


    def _fetch_data(self, parent_node):

        if parent_node.label() == "ROOT":
            if len(parent_node) != 1:
                return False
            return self._fetch_data(parent_node[0])

        if parent_node.label() == "SBARQ":
            if len(parent_node) < 2:
                return False

            whnp = False
            sq = False
            for node in parent_node:
                if node.label() == "WHNP":
                    whnp = self._fetch_data(node)

                if node.label() == "SQ":
                    sq = self._fetch_data(node)

            return whnp and sq

        if parent_node.label() == "WHNP":
            if len(parent_node) != 1:
                return False

            node = parent_node[0]
            if node.label() != "WP":
                return False

            return self._fetch_data(node)

        if parent_node.label() == "WP":
            if len(parent_node) != 1:
                return False

            word = parent_node[0]
            if word.lower() != "what":
                return False

            return True

        if parent_node.label() == "SQ":
            if len(parent_node) != 2:
                return False

            vb = False
            np = False
            for node in parent_node:
                if node.label() == "VBZ" or node.label() == "VBP":
                    vb = self._fetch_data(node)

                if node.label() == "NP":
                    np = self._fetch_data(node)

            return vb and np

        if parent_node.label() == "VBZ" or parent_node.label() == "VBP":
            if len(parent_node) != 1:
                return False
            return True

        if parent_node.label() == "NP":
            np = False
            pp = False
            for node in parent_node:
                if node.label() == "NP":
                    np = True
                    self._property = node

                if node.label() == "PP":
                    pp = self._fetch_data(node)

            return np and pp

        if parent_node.label() == "PP":
            if len(parent_node) != 2:
                return False

            intag = False
            np = False
            for node in parent_node:
                if node.label() == "IN":
                    intag = self._fetch_data(node)
                if node.label() == "NP":
                    np = True
                    self._object = node

            return intag and np

        if parent_node.label() == "IN":
            if len(parent_node) != 1:
                return False

            word = parent_node[0]
            if word.lower() != "of":
                return False

            return True


        return False

    def perform(self, tree):

        if not isinstance(tree, Tree):
            raise Exception("Wrong type of tree argument")

        self._tree = tree

        print(self._tree)
        # print(self._tree[0][0][0])
        if not self._fetch_data(self._tree):
            raise Exception()

        print(self._property)
        print(self._object)

        object_searcher = Object(self._object)
        object_searcher.find()
        print("FUCK!")

        pass

