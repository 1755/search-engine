import json
import urllib


# Search entity by string
def search(query):
        service_url = 'http://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbsearchentities',
            'search': str(query),
            'language': 'en',
            'format': 'json',
            'limit': 10,
        }

        url = service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())

        if response['success'] != 1:
            return None

        if 'search' not in response:
            return None

        return response['search']

# Get entity by id from wikibase
def get_entity(id):
    service_url = 'http://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbgetentities',
        'ids': str(id),
        'languages': 'en',
        'format': 'json',
        'limit': 1,
    }

    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())

    if response['success'] != 1:
        return None

    if 'entities' not in response:
        return None

    return response['entities'][response['entities'].keys()[0]]


# Convert property value(Pnnn) to human readbly value
def P2word(properties):
    def get(properties):
        service_url = 'http://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbgetentities',
            'ids': "|".join(properties),
            'languages': 'en',
            'props': 'labels',
            'format': 'json',
        }

        url = service_url + '?' + urllib.urlencode(params)
        # print(url)
        response = json.loads(urllib.urlopen(url).read())

        if response['success'] != 1:
            return None

        if 'entities' not in response:
            return None

        words = dict()
        for prop in properties:
            words[prop] = response['entities'][prop]['labels']['en']['value']

        return words

    max_prop_count = 50
    words = {}
    for i in xrange(0, 1+int(len(properties)/max_prop_count)):
        from_idx = i
        to_idx = (i+1)*max_prop_count

        words.update(get(properties[from_idx:to_idx]))

    return words


def make_items(search_result):
    items = []
    for result in search_result:

        entity = get_entity(result['id'])

        item = dict()

        try:
            item['labels'] = entity['labels']['en']['value']
        except KeyError:
            continue
        try:
            item['descriptions'] = entity['descriptions']['en']['value']
        except KeyError:
            pass

        item['statements'] = {}


        words = P2word(entity['claims'].keys())
        for claim in entity['claims']:
            statement = dict()
            statement['label'] = words[claim]
            statement['values'] = list()
            for value in entity['claims'][claim]:
                try:
                    statementval = dict()
                    statementval['data'] = value['mainsnak']['datavalue']
                    statementval['qualifiers'] = list()
                    # try:
                    #     statementval['qualifiers'] = value['qualifiers']
                    # except KeyError:
                    #     pass

                    statement['values'].append(statementval)
                except KeyError:
                    continue

            item['statements'][words[claim]] = statement

        items.append(item)

    return items


results = search("Earth")
items = make_items(results)
print(items)
print("ok")  # for breakpoint
