import json
import urllib

api_key = "AIzaSyCAkX3zgJ0PeVPtll935CwyN1E31VpCRnU"
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'
query = [{'id': None, 'name': None, 'type': '/astronomy/planet'}]
params = {
        'query': json.dumps(query),
        'key': api_key
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())


print response
# for planet in response['result']:
#   print planet['name']



query = 'volkov sergey'
filter = '(any type:/people/person domain:/film)'
service_url = 'https://www.googleapis.com/freebase/v1/search'
params = {
        'query': query,
        'key': api_key,
        'filter': filter
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
for result in response['result']:
    notable = ""
    try:
        notable = str(result['notable'])
    except KeyError:
        pass

    print result['name'] + ' (' + str(result['score']) + ')\t' + notable