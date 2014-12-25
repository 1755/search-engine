from nltk.tree import Tree
import json
import urllib


class Object:

    _object = None

    def __init__(self, object_tree):
        self._object = object_tree

    def find(self):
        nnp_node = self._extract_nnp(self._object)
        if not nnp_node:
            return False

        freebase_id, notable = self._make_search_query(" ".join(nnp_node.leaves()))
        print(freebase_id)
        print(notable)

        pass

    def _extract_nnp(self, parent_node):

        nnp_array = []
        for node in parent_node:
            if isinstance(node, Tree) and node.label() == "NNP":
                nnp_array.append("".join(node.leaves()))

        if len(nnp_array) > 0:
            return Tree("NP", nnp_array)

        for node in parent_node:
            if isinstance(node, Tree) and node.label() != "NNP":
                return self._extract_nnp(node)

        return False

    def _make_search_query(self, query):
        api_key = "AIzaSyCAkX3zgJ0PeVPtll935CwyN1E31VpCRnU"
        service_url = 'https://www.googleapis.com/freebase/v1/search'
        params = {
                'query': query,
                'key': api_key,
        }
        url = service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())

        for result in response['result']:
            notable = ""
            try:
                notable = str(result['notable'])
            except KeyError:
                pass
            return result['mid'], notable

