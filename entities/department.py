class Department:

    def __init__(self, name: str, uid: int = None):
        self.name = name
        self.id = uid

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
