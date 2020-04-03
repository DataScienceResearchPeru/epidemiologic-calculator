from injector import Binder

from repositories.i_user_repository import IUserRepository
from repositories.i_department_repository import IDepartmentRepository
from repositories.i_province_repository import IProvinceRepository
from repositories.i_district_repository import IDistrictRepository
from repositories.sqlalchemy.user_repository_sqlalchemy import UserRepositorySqlAlchemy
from repositories.sqlalchemy.department_repository_sqlalchemy import DepartmentRepositorySqlAlchemy
from repositories.sqlalchemy.province_repository_sqlalchemy import ProvinceRepositorySqlAlchemy
from repositories.sqlalchemy.district_repository_sqlalchemy import DistrictRepositorySqlAlchemy


def configure_repositories_binding(binder: Binder) -> Binder:
    binder.bind(IUserRepository, UserRepositorySqlAlchemy)
    binder.bind(IDepartmentRepository, DepartmentRepositorySqlAlchemy)
    binder.bind(IProvinceRepository, ProvinceRepositorySqlAlchemy)
    binder.bind(IDistrictRepository, DistrictRepositorySqlAlchemy)
    return binder
