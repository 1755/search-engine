# coding=utf-8
from nltk import Tree
from search_engine.components.data_base import DataBase
from search_engine.patterns.pattern import pattern
from search_engine.searchers.freebase import Freebase

__author__ = 'egres'


class ____of____(pattern):
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

            return [
                {'tree': self.get_query_tree()[0], 'context': 'PROPERTY'},
                {'tree': self.get_query_tree()[1][1], 'context': 'OBJECT'}
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



    def extract_answer(self, parts):

        object_part = None
        property_part = None
        for part in parts:
            if part['context'] == 'PROPERTY':
                property_part = part

            if part['context'] == 'OBJECT':
                object_part = part

        if object_part is None:
            return None

        if property_part is None:
            return None

        if 'data' not in object_part:
            return None

        if object_part['data'] is None:
            return None

        out_object_part = object_part.copy()
        out_object_part['data'] = dict()

        property_string = " ".join(property_part['tree'].leaves())
        for statement in object_part['data']['statements']:
            if statement == property_string:
                out_object_part['data'] = object_part['data']['statements'][statement]['values'][0]['data']['value'].copy()
                return [property_part, out_object_part]

        return None