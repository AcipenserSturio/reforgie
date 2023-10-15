class SqlInsert:
    def __init__(self, tablename, fields, iterable=None):
        self.tablename = tablename
        self.fields = fields

        if not iterable:
            # Create at least one row
            iterable = [None]

        self.rows = []
        for item in iterable:
            self.row(item)

    def row(self, *args):
        line = []
        for value in self.fields.values():
            if callable(value):
                value = value(*args)
            line.append(value)
        self.rows.append(str(tuple(line)))

    def to_str(self):
        return "\n".join([
            "INSERT INTO",
            self.tablename,
            str(tuple(self.fields.keys())),
            "VALUES",
            ",\n".join(self.rows) + ";"
        ])
