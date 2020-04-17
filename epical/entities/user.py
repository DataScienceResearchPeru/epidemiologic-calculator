import bcrypt

__all__ = ["User"]


class User:
    # FIX
    # Consider to move department, province and district id to another model
    # and preserver only escential information related to user.
    # pylint: disable=too-many-instance-attributes,

    def __init__(
        self,
        first_name: str,
        last_name: str,
        institution: str,
        email: str,
        password: str,
        department_id: int,
        province_id: int,
        district_id: int,
        confirm_email: bool,
        img_profile: str = None,
        uid: int = None,
    ):  # pylint: disable=too-many-arguments
        self.first_name = first_name
        self.last_name = last_name
        self.institution = institution
        self.email = email
        self.encrypted_password = bcrypt.hashpw(
            self.string_to_bit(password), bcrypt.gensalt()
        )
        self.confirm_email = confirm_email
        self.department_id = department_id
        self.province_id = province_id
        self.district_id = district_id
        self.img_profile = img_profile
        self.id = uid

    @staticmethod
    def string_to_bit(string):
        if isinstance(string, str):
            return string.encode("utf-8")
        return string

    def full_name(self):
        return self.first_name + " " + self.last_name

    def valid_credential(self, password: str):
        return bcrypt.checkpw(self.string_to_bit(password), self.encrypted_password)

    def change_password(self, password):
        self.encrypted_password = bcrypt.hashpw(
            self.string_to_bit(password), bcrypt.gensalt()
        )

    def active_email(self):
        self.confirm_email = True

    def is_active_email(self):
        return self.confirm_email

    def to_update(self, img_profile):  # pylint: disable=no-self-use
        return {
            "img_profile": img_profile,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "institution": self.institution,
            "img_profile": self.img_profile,
            "department_id": self.department_id,
            "province_id": self.province_id,
            "district_id": self.district_id,
        }
