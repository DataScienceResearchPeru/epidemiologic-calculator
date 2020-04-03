from sqlalchemy import Table, MetaData, Column, Integer, String, LargeBinary, Sequence, Boolean, DateTime, func, \
    ForeignKey
from sqlalchemy.orm import mapper

from entities.user import User


def user_mapping(metadata: MetaData):
    user = Table(
        'users',
        metadata,
        Column('id', Integer, Sequence('users_id_seq'), nullable=False, primary_key=True),
        Column('first_name', String(120)),
        Column('last_name', String(120)),
        Column('institution', String(200)),
        Column('email', String(120), unique=True),
        Column('encrypted_password', LargeBinary(60)),
        Column('confirm_email', Boolean),
        Column('departament_id', Integer, ForeignKey('departament.id')),
        Column('province_id', Integer, ForeignKey('province.id')),
        Column('district_id', Integer, ForeignKey('district.id')),
        Column('created_at', DateTime(), nullable=False, server_default=func.now()),
        Column('updated_at', DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())
    )

    mapper(User, user)

    return user
