import hashlib
class DB:
    def queryset_to_values(self, value1, value2=None):
        if value2 is None:
            return list(value1)
        else:
            return list(value1)[0][value2]

    def data_to_hash(self, value):
        value = hashlib.sha1(value.encode()).hexdigest()
        return value
