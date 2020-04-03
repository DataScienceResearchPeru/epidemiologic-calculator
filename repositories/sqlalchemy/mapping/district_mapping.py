from sqlalchemy import Table, MetaData, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import mapper, relationship

from entities.district import District
from entities.user import User


def district_mapping(metadata: MetaData):
    district = Table(
        'districts',
        metadata,
        Column('id', Integer, Sequence('districts_id_seq'), nullable=False, primary_key=True),
        Column('name', String(160), nullable=False),
        Column('province_id', Integer, ForeignKey('provinces.id'))
    )

    mapper(District, district, properties={
        'user': relationship(User, backref='district', order_by=district.c.id)
    })

    return district
