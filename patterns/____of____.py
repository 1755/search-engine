# coding=utf-8
from nltk import Tree
from search_engine.components.data_base import DataBase
from search_engine.patterns.pattern import pattern

__author__ = 'egres'


class ____of____(pattern):

    def __init__(self):
        self._object_part = None
        self._property_part = None
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

            self._property_part = self.get_query_tree()[0]
            self._object_part = self.get_query_tree()[1][1]
            return [
                {'tree': self._property_part, 'context': 'PROPERTY', 'data': {}},
                {'tree': self._object_part, 'context': 'OBJECT', 'data': {}}
            ]

        except IndexError:
            return None

    def search(self, parts):
        if parts is None:
            return None

        if len(parts) != 2:
            return None

        for part in parts:
            if 'tree' not in part:
                return None

        for part in parts:
            if part['context'] == 'PROPERTY':
                continue

            query = " ".join(part['tree'].leaves())
            db = DataBase()
            part['data'] = db.search(query)
            if part['data'] is None:
                return None

        return "some result"



    def extract_answer(self, data):

        property_string = " ".join(self._property_part.leaves())
        for statement in data['statements']:
            if statement == property_string:
                return data['statements'][statement]['values'][0]['data']['value'].copy()

        return None