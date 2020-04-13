__all__ = ["District"]


class District:
    def __init__(self, name: str, province_id: int, uid: int = None):
        self.name = name
        self.province_id = province_id
        self.id = uid

    def to_dict(self):
        return {"id": self.id, "name": self.name, "province_id": self.province_id}
