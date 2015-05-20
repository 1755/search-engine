from nltk import ParentedTree
from components.answer import Answer
from patterns import pattern_classes


class Parser:

    def __init__(self):
        self.answers = []

    def __extract(self, query_subtree, level=0):

        founded_answers = []
        for pattern_class in pattern_classes:
            pattern = pattern_class()
            part_list = pattern.match(query_subtree)
            if part_list is None or len(part_list) == 0:
                continue

            for part in part_list:
                object_from_database = pattern.search(part)
                if object_from_database is not None:
                    extracted_objects = pattern.extract_answer(part.property, object_from_database)
                    if extracted_objects:
                        for extracted_object in extracted_objects:
                            founded_answers.append(Answer(extracted_object, level))

                previous_founded = self.__extract(part.object, level+1)
                if len(previous_founded) > 0:
                    for answer in previous_founded:
                        extracted_objects = pattern.extract_answer(part.property, answer.data)
                        if extracted_objects:
                            for extracted_object in extracted_objects:
                                founded_answers.append(Answer(extracted_object, level+1))

        return founded_answers

    def run(self, query_tree):
        if not isinstance(query_tree, ParentedTree):
            raise AttributeError

        self.answers = self.__extract(query_tree)
        self.answers = sorted(self.answers, key=lambda answer: answer.score, reverse=True)
