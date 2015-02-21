# coding=utf-8
# Хотя не совсем абстрактные...


class AbstractValue(object):
    def value(self):
        raise NotImplementedError

    def __getitem__(self, item):
        if item == 'value':
            return self.value()
        else:
            raise KeyError


class AbstractProvider(object):
    def search(self, query):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError