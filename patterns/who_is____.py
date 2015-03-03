from search_engine.components.data_base import DataBase
from search_engine.patterns.pattern import pattern


class who_is____(pattern):

    def __init__(self):
        self._object_part_tree = None
        pattern.__init__(self)

    def match(self, *args, **kwargs):
        pattern.match(self, *args, **kwargs)
        try:
            if self.get_query_tree().label() != "ROOT":
                raise IndexError

            if self.get_query_tree()[0].label() != "SBARQ":
                raise IndexError

            if self.get_query_tree()[0][0].label() != "WHNP":
                raise IndexError

            if self.get_query_tree()[0][0][0].label() != "WP":
                raise IndexError

            if self.get_query_tree()[0][0][0][0].lower() != "who":
                raise IndexError

            if self.get_query_tree()[0][1].label() != "SQ":
                raise IndexError

            if len(self.get_query_tree()[0][1]) < 2:
                raise IndexError

            self._object_part_tree = self.get_query_tree()[0][1][1]
            return {
                pattern.CONTEXT_OBJECT: {
                    'tree': self._object_part_tree,
                    'context': pattern.CONTEXT_OBJECT,
                    'data': {}
                }
            }

        except IndexError:
            return None

    def search(self, parts):
        # @todo: check parts

        query = " ".join(parts[pattern.CONTEXT_OBJECT]['tree'].leaves())
        db = DataBase()
        parts[pattern.CONTEXT_OBJECT]['data'] = db.search(query)
        if parts[pattern.CONTEXT_OBJECT]['data'] is None:
            return None

        return True

    def extract_answer(self, data):
        return [data]