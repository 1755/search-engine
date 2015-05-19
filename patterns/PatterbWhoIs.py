from search_engine.patterns.PatternWhatIs import PatternWhatIs


class PatternWhoIs(PatternWhatIs):
    def __init__(self):
        super(PatternWhoIs, self).__init__()
        self._keyword = 'who'

    def extract_answer(self, property_tree, object_from_database):
        return [object_from_database]
        # todo: detect, which types corresponds to 'who'
        # if object_from_database is None:
        #     return []
        #
        # try:
        #     instance_of = object_from_database['statements']['instance of']
        #     for value in instance_of['values']:
        #         linked_object = value['data']['value']
        #         if linked_object['label'] == 'human':
        #             return [object_from_database]
        #
        #     return []
        # except KeyError as e:
        #     return []

