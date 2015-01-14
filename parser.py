from nltk import Tree
from search_engine.patterns import patterns
from search_engine.searchers.freebase import Freebase

__author__ = 'egres'


class Parser:

    answers = []

    def __init__(self):
        pass

    def __extract(self, query_tree, context='MAIN'):

        testdata = []
        for pattern in patterns:
            parts = pattern.match(query_tree=query_tree)
            if parts is None:
                continue

            if pattern.search(parts) is not None:
                print(pattern.__class__.__name__ + ".apply("+"str(parts)"+")")
                if context == 'MAIN':
                    self.answers.append(pattern.apply_data(parts))
                else:
                    d = pattern.apply_data(parts)
                    if d is not None:
                        testdata.append(d)

            prevdatas = []
            for part in parts:
                prevdata = self.__extract(part['tree'], part['context'])
                if prevdata:
                    prevdatas.append(prevdata)
                    # prevdatas.extend(prevdata)

            for prevdata in prevdatas:
                for data in prevdata:
                    print(pattern.__class__.__name__ + ".apply("+"str(parts)"+")")
                    if context == 'MAIN':
                        self.answers.append(pattern.apply_data(data))
                    else:
                        d = pattern.apply_data(data)
                        if d is not None:
                            testdata.append(d)

        return testdata


    def run(self, query_tree):

        if not isinstance(query_tree, Tree):
            raise AttributeError

        self.__extract(query_tree)

        pass
