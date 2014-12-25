import client
import sys
from nltk.tree import Tree
from extractors import extractors


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

            for extractor in extractors:
                try:
                    extractor.perform(tree)
                except Exception as e:
                    print(e.message)
                    pass






