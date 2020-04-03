import json

from entities.department import Department
from entities.province import Province
from entities.district import District
from repositories.sqlalchemy.department_repository_sqlalchemy import DepartmentRepositorySqlAlchemy
from repositories.sqlalchemy.province_repository_sqlalchemy import ProvinceRepositorySqlAlchemy
from repositories.sqlalchemy.district_repository_sqlalchemy import DistrictRepositorySqlAlchemy


def seed_departament(db, data):
    departament = Department(name=data['name'])
    try:
        departament_repository = DepartmentRepositorySqlAlchemy(db)
        departament_repository.add(departament)
    except Exception:
        raise


def seed_province(db, data):
    province = Province(name=data['name'], department_id=data['department_id'])
    try:
        province_repository = ProvinceRepositorySqlAlchemy(db)
        province_repository.add(province)
    except Exception:
        raise


def seed_district(db, data):
    district = District(name=data['name'], province_id=data['province_id'])
    try:
        district_repository = DistrictRepositorySqlAlchemy(db)
        district_repository.add(district)
    except Exception:
        raise


def seed_data(db):
    with open('seed.json', 'r') as json_data:
        data = json.load(json_data)
        for row in data["departments"]:
            seed_departament(db, row)
        for row in data["provinces"]:
            seed_province(db, row)
        for row in data["districts"]:
            seed_district(db, row)
