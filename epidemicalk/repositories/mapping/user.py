from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    MetaData,
    Sequence,
    String,
    Table,
    func,
)
from sqlalchemy.orm import mapper

from epidemicalk.entities.user import User


def user(metadata: MetaData):
    user = Table(
        "users",
        metadata,
        Column(
            "id", Integer, Sequence("users_id_seq"), nullable=False, primary_key=True
        ),
        Column("first_name", String(120)),
        Column("last_name", String(120)),
        Column("institution", String(200)),
        Column("email", String(120), unique=True),
        Column("encrypted_password", LargeBinary(60)),
        Column("confirm_email", Boolean),
        Column("img_profile", String(200)),
        Column("department_id", Integer, ForeignKey("departments.id")),
        Column("province_id", Integer, ForeignKey("provinces.id")),
        Column("district_id", Integer, ForeignKey("districts.id")),
        Column("created_at", DateTime(), nullable=False, server_default=func.now()),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )

    mapper(User, user)

    return user
