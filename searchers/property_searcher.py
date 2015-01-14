# coding=utf-8

# @todo скорее всего нужны будут регулярки тут.
properties_data = [
    {
        'name': 'the area',
        'notable': {
            'id': '/location/us_state',
            'text': 'US State'
        },
        'meaning': '/location/location/area'
    },
    {
        'name': 'the area',
        'notable': {
            'id': '/location/ru_federal_city',
            'text': 'Russian federal city'
        },
        'meaning': '/location/location/area'
    },
    {
        'name': 'the area',
        'notable': {
            'id': '/location/country',
            'text': 'Country'
        },
        'meaning': '/location/location/area'
    }

]


class PropertySearcher(object):
    def search(self, word, notable_for):
        if not notable_for['values']:
            return None

        for data in properties_data:
            if data['name'] == word and data['notable']['id'] == notable_for['values'][0]['id']:
                return data['meaning']

        return None