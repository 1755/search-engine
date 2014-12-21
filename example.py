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