from nltk import Tree
from search_engine.patterns.pattern import pattern

__author__ = 'egres'

properties_data = [
    {
        'name': 'the area',
        'notable': {
            'id': '/location/us_state',
            'text': 'US State'
        },
        'meaning': '/location/location/area'
    }
]


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

        if 'data' not in object_part:
            return None

        if property_part is None:
            return None

        if 'data' not in property_part:
            return None

        if object_part['data'] is None:
            return None

        if property_part['data'] is None:
            return None


        # ttt = Tree("NP", [])
        # ttt.leaves()
        notable_for = object_part['data']['property']['/common/topic/notable_for']
        prop = self.__word_to_property(" ".join(property_part['tree'].leaves()), notable_for)
        if prop is None:
            return None

        props_dict = object_part['data']['property'].copy()
        object_part['data']['property'] = {}

        for x in props_dict:
            if x == prop:
                object_part['data']['property'][x] = props_dict[x]

        return object_part

    def __word_to_property(self, word, notable):

        if not notable['values']:
            return None

        for data in properties_data:
            if data['name'] == word and data['notable']['id'] == notable['values'][0]['id']:
                return data['meaning']

        return None