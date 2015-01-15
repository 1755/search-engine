import copy

class Answer():
    data = None
    score = 0

    def __init__(self, data, score):
        if data is not None:
            self.data = copy.deepcopy(data)
        self.score = score
