from nltk import ParentedTree
from patterns.PatternPropertyOfObject import PatternPropertyOfObject
from patterns.pattern import Pattern


class PatternObjectSProperty(PatternPropertyOfObject):
    def walker(self, parent):
        if parent.label() == 'POS' and parent.leaves() == ["'s"]:
            pos = parent.parent().treeposition()

            a = parent.right_sibling()
            c = parent.left_sibling()
            b = self.get_query_tree()
            # part = Pattern.Part()
            # part.object = ParentedTree.fromstring(str(parent.right_sibling()))
            # part.property = ParentedTree.fromstring(str(self.get_query_tree()))
            # part.property[pos[:-1]].remove(part.property[pos])
            # self._parts.append(part)

        for child in parent:
            if isinstance(child, ParentedTree):
                self.walker(child)

    def match(self, *args, **kwargs):
        Pattern.match(self, *args, **kwargs)
        if self.get_query_tree().label() != 'NP':
            return []
        self.walker(self.get_query_tree())
        return self._parts