import json
import urllib


class Freebase(object):
    __api_key = "AIzaSyCAkX3zgJ0PeVPtll935CwyN1E31VpCRnU"

    def search(self, query, context=None):
        service_url = 'https://www.googleapis.com/freebase/v1/search'
        params = {
            'query': str(query),
            'key': self.__api_key,
        }

        url = service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())

        if response['status'] != "200 OK":
            return None

        result = response['result']
        result = filter(lambda x: 'notable' in x, result)
        if len(result) == 0:
            return None

        return result[0]

    def get_topic(self, id):
        service_url = 'https://www.googleapis.com/freebase/v1/topic'
        params = {
            'key': self.__api_key,
            'filter': 'allproperties'
        }
        url = service_url + id + '?' + urllib.urlencode(params)
        topic = json.loads(urllib.urlopen(url).read())
        if 'id' not in topic:
            return None

        return topic

    def mql(self, mkq_query):
        raise NotImplementedError