import json

from entities.department import Departament
from entities.province import Province
from entities.district import District
from repositories.sqlalchemy.departament_repository_sqlalchemy import DepartamentRepositorySqlAlchemy
from repositories.sqlalchemy.province_repository_sqlalchemy import ProvinceRepositorySqlAlchemy
from repositories.sqlalchemy.district_repository_sqlalchemy import DistrictRepositorySqlAlchemy


def seed_departament(db, data):
    departament = Departament(data['name'])
    try:
        departament_repository = DepartamentRepositorySqlAlchemy(db)
        departament_repository.add(departament)
    except Exception:
        raise


def seed_province(db, data):
    province = Province(data['name'], data['departament_id'])
    try:
        province_repository = ProvinceRepositorySqlAlchemy(db)
        province_repository.add(province)
    except Exception:
        raise


def seed_district(db, data):
    district = District(data['name'], data['province_id'])
    try:
        district_repository = DistrictRepositorySqlAlchemy(db)
        district_repository.add(district)
    except Exception:
        raise


def seed_data(db):
    with open('seed.json', 'r') as json_data:
        data = json.load(json_data)
        for row in data["departaments"]:
            seed_departament(db, row)
        for row in data["provinces"]:
            seed_province(db, row)
        for row in data["districts"]:
            seed_district(db, row)
