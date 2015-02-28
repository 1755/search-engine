import json
import urllib
from search_engine.components.data_base_providers.abstract_provider import *


class WikidataValue(AbstractValue):
    """
    Databalue provider for Wikidata
    """
    _type = None
    _value = None

    # @todo: consider all exists types
    def value(self):
        """
        Get value.

        :return: Value
        :rtype: dict
        """
        if self._type == 'string':
            return self.__get_string()
        elif self._type == 'quantity':
            return self.__get_quantity()
        elif self._type == 'time':
            return self.__get_time()
        elif self._type == 'wikibase-item':
            return self.__get_wikidata_item()
        else:
            return None

    def __get_string(self):
        return {
            'label': 'string',
            'description': 'string',
            'statements': self._value['value']
        }

    def __get_quantity(self):
        return {
            'label': 'quantity',
            'description': 'quantity',
            'statements': self._value['value']
        }

    def __get_time(self):
        return {
            'label': 'time',
            'description': 'time',
            'statements': self._value['value']
        }

    def __get_wikidata_item(self):
        wikidata_provider = WikidataProvider()
        return wikidata_provider.get('Q'+str(self._value['value']['numeric-id']))


class WikidataProvider(AbstractProvider):
    """
    Datasource provider for Wikidata
    """
    GET_ENTITIES_LIMIT = 50
    LANGUAGE = 'en'

    def search(self, query):
        """ Get structured entity by text query.

         :type query: str
         :param query: text query. If, for example, you want
            get some data for Moscow you can call:

                search("Moscow")

         :return: Entity which corresponded to query
         :rtype: dict
        """
        service_url = 'http://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbsearchentities',
            'search': str(query),
            'language': self.LANGUAGE,
            'format': 'json',
            'limit': 1,
        }

        url = service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())

        if 'success' not in response or response['success'] != 1:
            return None

        if 'search' not in response:
            return None

        if len(response['search']) <= 0:
            return None

        return self.get(response['search'][0]['id'])

    def get(self, id):
        """ Get structured entity by some identifier.
         :type entity_id: str
         :param entity_id: Identifier of entity

         :return: Entity which corresponded to id
         :rtype: dict
        """

        entities = self.__get_wb_entities([id])
        if entities is None or len(entities) <= 0:
            return None
        entity = entities[entities.keys()[0]]
        return self.__format_entity(entity)


    # @todo: use qualifiers
    def __format_entity(self, entity):
        item = dict()
        try:
            item['label'] = entity['labels']['en']['value']
        except KeyError:
            return None
        try:
            item['description'] = entity['descriptions']['en']['value']
        except KeyError:
            pass

        item['statements'] = {}


        words = self.__wb_properties_to_words(entity['claims'].keys())
        for claim in entity['claims']:
            statement = dict()
            statement['label'] = words[claim]
            statement['values'] = list()
            for value in entity['claims'][claim]:
                try:
                    statementval = dict()
                    data = WikidataValue()
                    data._type = value['mainsnak']['datatype']
                    data._value = value['mainsnak']['datavalue']
                    statementval['data'] = data
                    statementval['qualifiers'] = list()
                    # try:
                    #     statementval['qualifiers'] = value['qualifiers']
                    # except KeyError:
                    #     pass

                    statement['values'].append(statementval)
                except KeyError:
                    continue

            item['statements'][words[claim]] = statement

        return item

    def __get_wb_entities(self, ids):
        def get(ids):
            service_url = 'http://www.wikidata.org/w/api.php'
            params = {
                'action': 'wbgetentities',
                'ids': "|".join(ids),
                'languages': self.LANGUAGE,
                'format': 'json',
            }
            url = service_url + '?' + urllib.urlencode(params)
            response = json.loads(urllib.urlopen(url).read())

            if 'success' not in response or response['success'] != 1:
                return None

            if 'entities' not in response:
                return None

            return response['entities']

        entities = {}
        for i in xrange(0, 1+int(len(ids)/self.GET_ENTITIES_LIMIT)):
            from_idx = i
            to_idx = (i+1)*self.GET_ENTITIES_LIMIT

            entities.update(get(ids[from_idx:to_idx]))

        return entities

    def __wb_properties_to_words(self, ids):
        properties = self.__get_wb_entities(ids)
        words = {}

        # set default words
        for id in ids:
            words[id] = id

        for prop in properties:
            try:
                words[prop] = properties[prop]['labels'][self.LANGUAGE]['value']
            except KeyError:
                continue

        return words