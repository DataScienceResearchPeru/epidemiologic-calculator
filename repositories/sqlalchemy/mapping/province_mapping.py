from sqlalchemy import Table, MetaData, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import mapper, relationship

from entities.province import Province
from entities.district import District
from entities.user import User


def province_mapping(metadata: MetaData):
    province = Table(
        'provinces',
        metadata,
        Column('id', Integer, Sequence('provinces_id_seq'), nullable=False, primary_key=True),
        Column('name', String(160)),
        Column('departament_id', Integer, ForeignKey('departament.id'))
    )

    mapper(Province, province, properties={
        'district': relationship(District, backref='province', order_by=province.c.id),
        'user': relationship(User, backref='province', order_by=province.c.id)
    })

    return province
