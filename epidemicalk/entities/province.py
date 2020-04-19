__all__ = ["Province"]


class Province:
    def __init__(self, name: str, department_id: int, uid: int = None):
        self.name = name
        self.department_id = department_id
        self.id = uid

    def to_dict(self):
        return {"id": self.id, "name": self.name, "department_id": self.department_id}
