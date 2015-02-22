from search_engine.components.data_base import DataBase
from search_engine.patterns import pattern

__author__ = 'Volkov Sergey'


class what_is____(pattern.pattern):
    def match(self, *args, **kwargs):
        pattern.pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != "ROOT":
                raise IndexError

            if self.get_query_tree()[0].label() != "SBARQ":
                raise IndexError

            if self.get_query_tree()[0][0].label() != "WHNP":
                raise IndexError

            if self.get_query_tree()[0][0][0].label() != "WP":
                raise IndexError

            if self.get_query_tree()[0][0][0][0].lower() != "what":
                raise IndexError

            if self.get_query_tree()[0][1].label() != "SQ":
                raise IndexError

            if self.get_query_tree()[0][1][0].label() != "VBZ":
                raise IndexError

            if self.get_query_tree()[0][1][1].label() != "NP":
                raise IndexError

            return [{
                        'tree': self.get_query_tree()[0][1][1],
                        'context': self.CONTEXT_OBJECT
                    }]

        except IndexError:
            return None

    def search(self, parts):
        if parts is None:
            return None

        if len(parts) == 0:
            return None

        if 'tree' not in parts[0]:
            return None

        query = " ".join(parts[0]['tree'].leaves())
        db = DataBase()
        parts[0]['data'] = db.search(query)
        if parts[0]['data'] is None:
            return None

        return "some result"


    def extract_answer(self, data):
        return data