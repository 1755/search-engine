from nltk import Tree
from search_engine.components.answer import Answer
from search_engine.patterns import patterns

class Parser:

    answers = []

    def __init__(self):
        self.answers = []

    def __extract(self, query_tree, context='MAIN', level=0):

        founded = []
        for pattern in patterns:
            parts = pattern.match(query_tree=query_tree)
            if parts is None:
                continue

            if pattern.search(parts):
                obj = None
                for part in parts:
                    if part['context'] == 'OBJECT':
                        obj = part

                data = pattern.extract_answer(obj['data'])
                if data:
                    founded.append(Answer(data, level))

            for part in parts:
                prevfounded = self.__extract(part['tree'], part['context'], level+1)
                if len(prevfounded) > 0:
                    for item in prevfounded:
                        data = pattern.extract_answer(item.data)
                        if data:
                            founded.append(Answer(data, level+1))


        return founded


    def run(self, query_tree):

        if not isinstance(query_tree, Tree):
            raise AttributeError

        self.answers = self.__extract(query_tree)
        self.answers = sorted(self.answers, key=lambda answer: answer.score, reverse=True)

        pass
