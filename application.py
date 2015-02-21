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
                print("SCORE: " + str(answer.score)+" ==========================")
                print("Label: "+str(answer.data['data']['label']))
                print("Properties:")
                for prop in answer.data['data']['statements']:
                    try:
                        print("\t"+str(prop))
                    except Exception:
                        pass
                print("\n\n")

            del parser