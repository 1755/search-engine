# coding=utf-8
from nltk import ParentedTree
from search_engine.components.data_base import DataBase
from search_engine.components.property_finder import PropertyFinder
from search_engine.patterns.pattern import Pattern


class PatternPropertyOfObject(Pattern):

    def __init__(self):
        self._parts = []
        super(Pattern, self).__init__()

    def walker(self, parent):
        if parent.label() == 'IN':
            pos = parent.parent().treeposition()

            part = Pattern.Part()
            part.object = ParentedTree.fromstring(str(parent.right_sibling()))
            part.property = ParentedTree.fromstring(str(self.get_query_tree()))
            part.property[pos[:-1]].remove(part.property[pos])
            self._parts.append(part)

        for child in parent:
            if isinstance(child, ParentedTree):
                self.walker(child)

    def match(self, *args, **kwargs):
        Pattern.match(self, *args, **kwargs)
        self.walker(self.get_query_tree())
        return self._parts

    def search(self, part):
        query = " ".join(part.object.leaves())
        return DataBase().search(query)

    def extract_answer(self, property_tree, object_from_database):

        founded_items = []
        property_finder = PropertyFinder()
        candidates = property_finder.find_candidates(property_tree)
        for statement in object_from_database['statements']:
            if statement in candidates:
                for value in object_from_database['statements'][statement]['values']:
                    tmp = value['data']['value']
                    if tmp:
                        founded_items.append(tmp.copy())

        return founded_items