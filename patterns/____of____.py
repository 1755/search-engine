# coding=utf-8
from nltk import Tree
from search_engine.patterns.pattern import pattern
from search_engine.searchers.property_searcher import PropertySearcher

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

        if len(parts) == 0:
            return None

        for part in parts:
            if 'tree' not in part:
                return None

        for part in parts:
            if part['context'] == 'PROPERTY':
                continue

            result = self._freebase.search(" ".join(part['tree'].leaves()))
            if result is None:
                return None

            part['data'] = self._freebase.get_topic(result['mid'])
            if part['data'] is None:
                return None

        return "some result"



    def apply_data(self, parts):

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

        notable_for = object_part['data']['property']['/common/topic/notable_for']
        prop = PropertySearcher().search(" ".join(property_part['tree'].leaves()), notable_for)
        if prop is None:
            return None

        props_dict = object_part['data']['property'].copy()
        object_part['data']['property'] = {}

        for x in props_dict:
            if x == prop:
                object_part['data']['property'][x] = props_dict[x]
            if x == '/common/topic/notable_for':
                # @todo: определить, какие свойства всегда оставлять
                object_part['data']['property'][x] = props_dict[x]

        return [property_part, object_part]