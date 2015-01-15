from nltk import Tree
from search_engine.components.answer import Answer
from search_engine.patterns import patterns
from search_engine.searchers.freebase import Freebase

__author__ = 'egres'


class Parser:

    answers = []

    def __init__(self):
        pass

    def __extract(self, query_tree, context='MAIN', level=0):

        testdata = []
        for pattern in patterns:
            parts = pattern.match(query_tree=query_tree)
            if parts is None:
                continue

            if pattern.search(parts) is not None:
                print(pattern.__class__.__name__ + ".apply("+"str(parts)"+")")
                if context == 'MAIN':
                    answer = Answer(pattern.apply_data(parts), 0)
                    self.answers.append(answer)
                else:
                    answer = Answer(pattern.apply_data(parts), level)
                    if answer.data is not None:
                        testdata.append(answer)

            prevdatas = []
            for part in parts:
                prevdata = self.__extract(part['tree'], part['context'], level + 1)
                if prevdata:
                    prevdatas.append(prevdata)

            for prevdata in prevdatas:
                for prevanswer in prevdata:
                    print(pattern.__class__.__name__ + ".apply("+"str(parts)"+")")
                    if context == 'MAIN':
                        answer = Answer(pattern.apply_data(prevanswer.data), prevanswer.score)
                        self.answers.append(answer)
                    else:
                        answer = Answer(pattern.apply_data(prevanswer.data), level)
                        if answer.data is not None:
                            testdata.append(answer)

        return testdata


    def run(self, query_tree):

        if not isinstance(query_tree, Tree):
            raise AttributeError

        self.__extract(query_tree)

        self.answers = sorted(self.answers, key=lambda answer: answer.score, reverse=True)

        pass
