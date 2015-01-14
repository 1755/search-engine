import client
import sys
from nltk.tree import Tree
from search_engine.parser import Parser

class Application:

    def __init__(self):
        pass

    def run(self):
        nlp = client.StanfordNLP()
        while True:
            print "Enter question: "
            question = sys.stdin.readline()

            result = nlp.parse(question)

            try:
                tree = Tree.fromstring(result['sentences'][0]['parsetree'])
            except IndexError:
                continue

            parser = Parser()
            parser.run(tree)

            for answer in parser.answers:
                print("ANSWER==========================")
                for prop in answer['data']['property']:
                    try:
                        print(prop)
                        for value in answer['data']['property'][prop]['values']:
                            print("\t"+value['text'])

                    except Exception:
                        pass
                print("\n\n")







