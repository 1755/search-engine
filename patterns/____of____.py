# coding=utf-8
from search_engine.components.data_base import DataBase
from search_engine.patterns.pattern import pattern


class ____of____(pattern):

    def __init__(self):
        self._object_part_tree = None
        self._property_part_tree = None
        pattern.__init__(self)

    def match(self, *args, **kwargs):
        pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != "NP":
                raise IndexError

            if self.get_query_tree()[0].label() != "NP":
                raise IndexError

            if self.get_query_tree()[1].label() != "PP":
                raise IndexError

            if self.get_query_tree()[1][0].label() != "IN":
                raise IndexError

            if self.get_query_tree()[1][0][0].lower() != "of":
                raise IndexError

            self._property_part_tree = self.get_query_tree()[0]
            self._object_part_tree = self.get_query_tree()[1][1]
            return {
                pattern.CONTEXT_PROPERTY: {
                    'tree': self._property_part_tree,
                    'context': pattern.CONTEXT_PROPERTY,
                    'data': {}
                },
                pattern.CONTEXT_OBJECT: {
                    'tree': self._object_part_tree,
                    'context': pattern.CONTEXT_OBJECT,
                    'data': {}
                }
            }

        except IndexError:
            return None

    def search(self, parts):
        # @todo: check parts

        query = " ".join(parts[pattern.CONTEXT_OBJECT]['tree'].leaves())
        db = DataBase()
        parts[pattern.CONTEXT_OBJECT]['data'] = db.search(query)
        if parts[pattern.CONTEXT_OBJECT]['data'] is None:
            return None

        return True

    def extract_answer(self, data):

        founded_items = []
        property_string = " ".join(self._property_part_tree.leaves())
        for statement in data['statements']:
            if statement == property_string:
                for value in data['statements'][statement]['values']:
                    data = value['data']['value']
                    if data:
                        founded_items.append(data.copy())

        return founded_items