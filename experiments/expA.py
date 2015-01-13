# coding=utf-8
import json
import pickle
import urllib
from search_engine import client
import sys
from nltk.tree import Tree
import zmq

nlp = client.StanfordNLP()


def match___between___(tree):
    try:
        if tree.label() != "NP":
            raise IndexError

        if tree[0].label() != "NP":
            raise IndexError

        if tree[1].label() != "PP":
            raise IndexError

        if tree[1][0].label() != "IN":
            raise IndexError

        if tree[1][0][0].lower() != "between":
            raise IndexError

        if tree[1][1].label() != "NP":
            raise IndexError

        a = []
        b = []
        is_cc_finded = False
        for node in tree[1][1]:
            if node.label() == "CC":
                if node[0].lower() == "and":
                    is_cc_finded = True
                continue

            if not is_cc_finded:
                a.append(node)
            else:
                b.append(node)

        if not is_cc_finded:
            raise IndexError

        if len(a) <= 0 or len(b) <= 0:
            raise IndexError

        if len(a) == 1:
            tree_a = Tree('NP', a[0])
        else:
            tree_a = Tree('NP', a)

        if len(b) == 1:
            tree_b = Tree('NP', b[0])
        else:
            tree_b = Tree('NP', b)

        return [tree[0], tree_a, tree_b], ['PROPERTY', 'OBJECT_A', 'OBJECT_B']

    except Exception:
        return False, []


def match___of___(tree):
    try:
        if tree.label() != "NP":
            raise IndexError

        if tree[0].label() != "NP":
            raise IndexError

        if tree[1].label() != "PP":
            raise IndexError

        if tree[1][0].label() != "IN":
            raise IndexError

        if tree[1][0][0].lower() != "of":
            raise IndexError

        return [tree[0], tree[1][1]], ['PROPERTY', 'OBJECT']

    except Exception:
        return False, []


def match_what_is___(tree):
    try:
        if tree.label() != "ROOT":
            raise IndexError

        if tree[0].label() != "SBARQ":
            raise IndexError

        if tree[0][0].label() != "WHNP":
            raise IndexError

        if tree[0][0][0].label() != "WP":
            raise IndexError

        if tree[0][0][0][0].lower() != "what":
            raise IndexError

        if tree[0][1].label() != "SQ":
            raise IndexError

        if tree[0][1][0].label() != "VBZ":
            raise IndexError

        if tree[0][1][1].label() != "NP":
            raise IndexError

        return [tree[0][1][1]], ['OBJECT']

    except Exception:
        return False, []


def search(query):
    api_key = "AIzaSyCAkX3zgJ0PeVPtll935CwyN1E31VpCRnU"
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    params = {
        'query': query,
        'key': api_key,
    }
    url = service_url + '?' + urllib.urlencode(params)
    response = json.loads(urllib.urlopen(url).read())
    return response['result'][0] if response['result'] else False


def load_object(mid):
    api_key = "AIzaSyCAkX3zgJ0PeVPtll935CwyN1E31VpCRnU"

    service_url = 'https://www.googleapis.com/freebase/v1/topic'
    params = {
        'key': api_key,
        'filter': 'allproperties'
    }
    url = service_url + mid + '?' + urllib.urlencode(params)
    topic = json.loads(urllib.urlopen(url).read())

    # for property in topic['property']:
    #     print property + ':'
    #     for value in topic['property'][property]['values']:
    #         try:
    #             print ' - ' + value['text']
    #         except Exception:
    #             pass

    return topic


# Составить базу данных
def property_to_field(property):
    if not isinstance(property, dict):
        return None

    if property['id'] == '/m/0n0j':
        return '/location/location/area'

    if property['id'] == '/m/0mnq':
        return '/base/natlang/abbreviated_topic/abbreviations'


patterns = [match_what_is___, match___of___, match___between___]
def test(tree, tree_type=None, level=0):
    if not isinstance(tree, Tree):
        pass

    print("\nLevel: " + str(level) + ", tree:" + str(tree.flatten()))
    is_time_to_search = True
    for pattern in patterns:
        result,types = pattern(tree)
        print("Pattern: " + str(pattern.__name__) + ", result: " + str(result))
        if result:
            is_time_to_search = False
            values = {}
            for part, type in zip(result, types):
                values[str(type)] = test(part, type, level + 1)


            if pattern == match___between___:

                property = values['PROPERTY']
                object_a = values['OBJECT_A']
                object_b = values['OBJECT_B']

                return object_a

            if pattern == match_what_is___:
                object = values['OBJECT']
                return object

            if pattern == match___of___:
                property = values['PROPERTY']
                tee = property_to_field(property)
                object = values['OBJECT'].copy()
                object['property'] = {}
                for property in values['OBJECT']['property']:
                    if property == tee:
                        object['property'][property] = values['OBJECT']['property'][property]

                return object

    if is_time_to_search:
        if tree_type == 'PROPERTY':
            property_tree = tree
            for i in xrange(len(property_tree)):
                if property_tree[i].label() == "DT":
                    del property_tree[i]
                    break  # stupid solution

            name = property_tree.flatten()[0]
            name = name.replace(' ', '_')
            topic = load_object('/en/'+name)
            return topic

        if tree_type[:len('OBJECT')] == 'OBJECT':
            search_item = search(tree.flatten()[0])
            if search_item:
                topic = load_object(search_item['mid'])
                # for value in topic['property']['/common/topic/description']['values']:
                #     print value['value']

                return topic

            return False


def answer(freebase_object):
    if not isinstance(freebase_object, dict):
        return "I know nothing"

    has_answer = False
    ansstring = ""
    for property in freebase_object['property']:
        ansstring += property + ':'  + "\n"
        for value in freebase_object['property'][property]['values']:
            try:
                ansstring += ' - ' + value['text'] + "\n"
                has_answer = True
            except Exception:
                pass

    if not has_answer:
        return "I know nothing"

    return ansstring


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://127.0.0.1:5001')

while True:
    # print("Enter question:")
    # question = sys.stdin.readline()
    print("Wait question")
    question = pickle.loads(socket.recv())
    print("Recieved: "+question)
    tree = False
    result = nlp.parse(question)



    try:
        tree = Tree.fromstring(result['sentences'][0]['parsetree'])
    except IndexError:
        continue

    if not tree:
        continue

    answer_string = answer(test(tree))
    print(answer_string)
    socket.send(pickle.dumps(answer_string))


