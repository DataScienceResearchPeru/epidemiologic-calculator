import bcrypt


class User:

    def __init__(self, first_name: str, last_name: str, institution: str, email: str, password: str,
                 department_id: int, province_id: int, district_id: int, confirm_email: bool, uid: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.institution = institution
        self.email = email
        self.encrypted_password = bcrypt.hashpw(self.string_to_bit(password), bcrypt.gensalt())
        self.confirm_email = confirm_email
        self.department_id = department_id
        self.province_id = province_id
        self.district_id = district_id
        self.id = uid

    @staticmethod
    def string_to_bit(string):
        if type(string) is str:
            return string.encode('utf-8')
        return string

    def full_name(self):
        return self.first_name + " " + self.last_name

    def valid_credential(self, password: str):
        return bcrypt.checkpw(self.string_to_bit(password), self.encrypted_password)

    def change_password(self, password):
        self.encrypted_password = bcrypt.hashpw(self.string_to_bit(password), bcrypt.gensalt())

    def active_email(self):
        self.confirm_email = True

    def is_active_email(self):
        return self.confirm_email

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'institution': self.institution,
            'department_id': self.department_id,
            'province_id': self.province_id,
            'district_id': self.district_id
        }
