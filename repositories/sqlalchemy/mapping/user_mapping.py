from sqlalchemy import Table, MetaData, Column, Integer, String, LargeBinary, Sequence, Boolean
from sqlalchemy.orm import mapper

from entities.user import User


def user_mapping(metadata: MetaData):
    user = Table(
        'users',
        metadata,
        Column('id', Integer, Sequence('users_id_seq'), nullable=False, primary_key=True),
        Column('first_name', String(120)),
        Column('last_name', String(120)),
        Column('email', String(120), unique=True),
        Column('encrypted_password', LargeBinary(60)),
        Column('confirm_email', Boolean)
    )

    mapper(User, user)

    return user
