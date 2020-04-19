from sqlalchemy import Column, ForeignKey, Integer, MetaData, Sequence, String, Table
from sqlalchemy.orm import mapper, relationship

from epidemicalk.entities.district import District
from epidemicalk.entities.province import Province
from epidemicalk.entities.user import User


def province(metadata: MetaData):
    province = Table(
        "provinces",
        metadata,
        Column(
            "id",
            Integer,
            Sequence("provinces_id_seq"),
            nullable=False,
            primary_key=True,
        ),
        Column("name", String(160), nullable=False, unique=True),
        Column("department_id", Integer, ForeignKey("departments.id")),
    )

    mapper(
        Province,
        province,
        properties={
            "district": relationship(
                District, backref="province", order_by=province.c.id
            ),
            "user": relationship(User, backref="province", order_by=province.c.id),
        },
    )

    return province
