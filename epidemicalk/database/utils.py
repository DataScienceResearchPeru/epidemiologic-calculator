import json

from epidemicalk.entities import Department, District, Province
from epidemicalk.repositories.department import DepartmentRepository
from epidemicalk.repositories.district import DistrictRepository
from epidemicalk.repositories.province import ProvinceRepository


def seed_department(db, data):
    department = Department(name=data["name"])
    department_repository = DepartmentRepository(db)
    department_repository.add(department)


def seed_province(db, data):
    province = Province(name=data["name"], department_id=data["department_id"])
    province_repository = ProvinceRepository(db)
    province_repository.add(province)


def seed_district(db, data):
    district = District(name=data["name"], province_id=data["province_id"])
    district_repository = DistrictRepository(db)
    district_repository.add(district)


def seed_data(db):
    with open("seed.json", "r") as json_data:
        data = json.load(json_data)
        for row in data["departments"]:
            seed_department(db, row)
        for row in data["provinces"]:
            seed_province(db, row)
        for row in data["districts"]:
            seed_district(db, row)
