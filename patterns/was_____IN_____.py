from search_engine.components.data_base import DataBase
from search_engine.patterns.pattern import pattern


class was____IN____(pattern):

    test_properties = {
        'written by': 'notable works'
    }

    def __init__(self):
        self._object_part_tree = None
        self._verb_part_tree = None
        self._in_part_tree = None
        pattern.__init__(self)

    def match(self, *args, **kwargs):
        pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != 'VP':
                raise IndexError

            if self.get_query_tree()[0].label() != "VBN":
                raise IndexError

            if self.get_query_tree()[1].label() != "PP":
                raise IndexError

            if self.get_query_tree()[1][0].label() != "IN":
                raise IndexError

            if self.get_query_tree()[1][1].label() != "NP":
                raise IndexError

            self._object_part_tree = self.get_query_tree()[1][1]
            self._verb_part_tree = self.get_query_tree()[0]
            self._in_part_tree = self.get_query_tree()[1][0]

            return [
                {'tree': self._verb_part_tree, 'context': pattern.CONTEXT_vEB, 'data': {}},
                {'tree': self._object_part_tree, 'context': pattern.CONTEXT_OBJECT, 'data': {}},
                {'tree': self._in_part_tree, 'context': pattern.CONTEXT_IN, 'data': {}}
            ]

        except IndexError:
            return None

    def search(self, parts):
        if parts is None:
            return None

        if len(parts) != 3:
            return None

        for part in parts:
            if 'tree' not in part:
                return None

        for part in parts:
            if part['context'] != pattern.CONTEXT_OBJECT:
                continue

            query = " ".join(part['tree'].leaves())
            db = DataBase()
            part['data'] = db.search(query)
            if part['data'] is None:
                return None

        return True

    def extract_answer(self, data):

        founded_items = []

        property_key = " ".join(self._verb_part_tree.leaves()) + " " + " ".join(self._in_part_tree.leaves())
        try:
            property_string = self.test_properties[property_key]
        except KeyError:
            return founded_items

        for statement in data['statements']:
            if statement == property_string:
                for value in data['statements'][statement]['values']:
                    founded_items.append(value['data']['value'].copy())

        return founded_items