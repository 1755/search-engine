import os
import nltk
import client
import sys
from nltk.tree import ParentedTree
from search_engine.parser import Parser
from search_engine.components.property_finder import PropertyFinder

class Application(object):
    def __init__(self):
        self._nlp = client.StanfordNLP()
        # nltk.data.path.append(str(os.path.abspath('./../nltk_data')))
        nltk.data.path.append(str(os.path.abspath('/home/egres/wokrspace/EIFSDB/nltk_data')))
        pass

    def get_answer(self, question):
        result = self._nlp.parse(question)

        try:
            tree = ParentedTree.fromstring(result['sentences'][0]['parsetree'])
        except IndexError or KeyError:
            return None

        parser = Parser()
        parser.run(tree)
        answers = parser.answers
        del parser
        return answers

    def run(self):

        while True:
            print "Enter question: "
            question = sys.stdin.readline()
            answers = self.get_answer(question)
            for answer in answers:
                print("SCORE: " + str(answer.score)+" ==========================")
                print("Label: "+str(answer.data['label'].encode('utf-8')))
                try:
                    print("Description: "+str(answer.data['description'].encode('utf-8')))
                except KeyError:
                    pass

                print("Properties:")
                for prop in answer.data['statements']:
                    try:
                        print("\t"+str(prop.encode('utf-8')))
                        for value in answer.data['statements'][prop]['values']:
                             tmp = value['data'].value()
                             print("\t\t"+value['data'].value()['label'])
                    except Exception:
                        pass
                print("\n\n")