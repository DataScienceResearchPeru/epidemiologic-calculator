from sqlalchemy import Column, Integer, MetaData, Sequence, String, Table
from sqlalchemy.orm import mapper, relationship

from epidemicalk.entities.department import Department
from epidemicalk.entities.province import Province
from epidemicalk.entities.user import User


def department(metadata: MetaData):
    department = Table(
        "departments",
        metadata,
        Column(
            "id",
            Integer,
            Sequence("departments_id_seq"),
            nullable=False,
            primary_key=True,
        ),
        Column("name", String(160), nullable=False, unique=True),
    )

    mapper(
        Department,
        department,
        properties={
            "province": relationship(
                Province, backref="department", order_by=department.c.id
            ),
            "user": relationship(User, backref="department", order_by=department.c.id),
        },
    )

    return department
