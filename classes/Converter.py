class DB:
    def queryset_to_values(self, value1, value2=None):
        if value2 is None:
            return list(value1)
        else:
            return list(value1)[0][value2]
