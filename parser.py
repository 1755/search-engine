from nltk import Tree
from search_engine.components.answer import Answer
from search_engine.patterns import pattern_classes


class Parser:

    def __init__(self):
        self.answers = []

    def __extract(self, query_tree, level=0):

        founded_answers = []
        for pattern_class in pattern_classes:
            pattern = pattern_class()
            parts = pattern.match(query_tree)
            if parts is None:
                continue

            if pattern.search(parts):
                obj = None
                for part in parts:
                    if part['context'] == 'OBJECT':
                        obj = part

                items = pattern.extract_answer(obj['data'])
                if items:
                    for item in items:
                        founded_answers.append(Answer(item, level))

            for part in parts:
                previous_founded = self.__extract(part['tree'], level+1)
                if len(previous_founded) > 0:
                    for item in previous_founded:
                        items = pattern.extract_answer(item.data)
                        if items:
                            for item in items:
                                founded_answers.append(Answer(item, level+1))

        return founded_answers


    def run(self, query_tree):

        if not isinstance(query_tree, Tree):
            raise AttributeError

        self.answers = self.__extract(query_tree)
        self.answers = sorted(self.answers, key=lambda answer: answer.score, reverse=True)
