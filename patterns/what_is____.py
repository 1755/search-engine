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

        result = self._freebase.search(" ".join(parts[0]['tree'].leaves()))
        if result is None:
            return None

        parts[0]['data'] = self._freebase.get_topic(result['mid'])
        if parts[0]['data'] is None:
            return None

        return "some result"


    def apply_data(self, parts):
        object_part = None
        for part in parts:
            if part['context'] == self.CONTEXT_OBJECT:
                object_part = part

        if object_part is None:
            return None

        if 'data' not in object_part:
            return None

        if object_part['data'] is None:
            return None

        return object_part