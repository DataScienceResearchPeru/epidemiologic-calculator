import bcrypt


class User:

    def __init__(self, first_name: str, last_name: str, institution: str, email: str, password: str, confirm_email: bool = True):
        self.first_name = first_name
        self.last_name = last_name
        self.institution = institution
        self.email = email
        self.encrypted_password = bcrypt.hashpw(self.string_to_bit(password), bcrypt.gensalt())
        self.confirm_email = confirm_email

    @staticmethod
    def string_to_bit(string):
        if type(string) is str:
            return string.encode('utf-8')
        return string

    def valid_credential(self, password: str):
        return bcrypt.checkpw(self.string_to_bit(password), self.encrypted_password)

    def change_password(self, password):
        self.encrypted_password = bcrypt.hashpw(self.string_to_bit(password), bcrypt.gensalt())

    def data(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'institution': self.institution
        }
