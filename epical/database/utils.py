import json

from epical.entities import Department, District, Province
from epical.repositories.department import DepartmentRepository
from epical.repositories.district import DistrictRepository
from epical.repositories.province import ProvinceRepository


def seed_department(db, data):
    department = Department(name=data["name"])
    department_repository = DepartmentRepository(db)
    department_repository.add(department)
    # FIX:
    # If the exception is not handled, don't use try except blocks
    # try:
    #     department_repository = DepartmentRepository(db)
    #     department_repository.add(department)
    # except Exception:
    #     raise


def seed_province(db, data):
    province = Province(name=data["name"], department_id=data["department_id"])
    province_repository = ProvinceRepository(db)
    province_repository.add(province)
    # FIX:
    # If the exception is not handled, don't use try except blocks
    # try:
    #     province_repository = ProvinceRepository(db)
    #     province_repository.add(province)
    # except Exception:
    #     raise


def seed_district(db, data):
    district = District(name=data["name"], province_id=data["province_id"])
    district_repository = DistrictRepository(db)
    district_repository.add(district)
    # FIX:
    # If the exception is not handled, don't use try except blocks
    # try:
    #     district_repository = DistrictRepository(db)
    #     district_repository.add(district)
    # except Exception:
    #     raise


def seed_data(db):
    with open("seed.json", "r") as json_data:
        data = json.load(json_data)
        for row in data["departments"]:
            seed_department(db, row)
        for row in data["provinces"]:
            seed_province(db, row)
        for row in data["districts"]:
            seed_district(db, row)
