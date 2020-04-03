from sqlalchemy import Table, MetaData, Column, Integer, String, Sequence
from sqlalchemy.orm import mapper, relationship

from entities.department import Departament
from entities.province import Province
from entities.user import User


def departament_mapping(metadata: MetaData):
    departament = Table(
        'departaments',
        metadata,
        Column('id', Integer, Sequence('departaments_id_seq'), nullable=False, primary_key=True),
        Column('name', String(160))
    )

    mapper(Departament, departament, properties={
        'province': relationship(Province, backref='departament', order_by=departament.c.id),
        'user': relationship(User, backref='departament', order_by=departament.c.id)
    })

    return departament
