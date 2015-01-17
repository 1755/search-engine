import re
# coding=utf-8

# @todo скорее всего нужны будут регулярки тут.
properties_data = [
    {
        'name': 'the area',
        'notable': r'/location/[a-z/?]',
        'meaning': '/location/location/area'
    },
    {
        'name': 'area',
        'notable': r'/location/[a-z/?_]',
        'meaning': '/location/location/area'
    },
]


class PropertySearcher(object):
    def search(self, word, notable_for):
        if not notable_for['values']:
            return None

        for data in properties_data:
            comparator = re.compile(data['notable'])
            if data['name'] == word and comparator.match(notable_for['values'][0]['id']):
                return data['meaning']

        return None