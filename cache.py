"""
In-memory caching of key-value pairs with extra keys.

"""


class Cache:
    """
    Implements a flexible generic storage mechanism with multiple indexes to access data.

    """

    def __init__(self, name):
        self.name = name
        self.data = {}
        self.index = {}

    def clear(self):
        self.index = {}
        self.data = {}

    def add(self, pk, value, extrakeys=None):
        try:
            self.data[pk] = value
            if extrakeys is not None:
                for k in extrakeys.keys():
                    if k not in self.index:
                        self.index[k] = {}
                    v = extrakeys[k]
                    if v not in self.index[k]:
                        self.index[k][v] = [pk]
                    else:
                        self.index[k][v].append(pk)
        except IndexError as e:
            print(f"Cache {self.name} add error {e} pk:{pk} extrakeys: {extrakeys} value {value}")

    def get(self, pk):
        return self.data[pk]

    def get_with_default(self, pk, default=None):
        if pk not in self.data:
            return default
        return self.data[pk]

    def get_by_unique_key(self, key, value):
        print(f'cache: {self.name} get_by_unique_key({key}, {value})')
        if key not in self.index:
            return None
        if value not in self.index[key]:
            return None
        keylist = self.index[key][value]
        if len(keylist) != 1:
            return None
        return self.data[keylist[0]]

    def list_by_key(self, key, value):
        if key not in self.index:
            return None
        if value not in self.index[key]:
            return None
        keylist = self.index[key][value]
        valuelist = []
        for pk in keylist:
            valuelist.append(self.data[pk])
        return valuelist
