from injector import Binder

from epidemicalk.repositories.department import (
    DepartmentRepository,
    DepartmentRepositoryInterface,
)
from epidemicalk.repositories.district import (
    DistrictRepository,
    DistrictRepositoryInterface,
)
from epidemicalk.repositories.province import (
    ProvinceRepository,
    ProvinceRepositoryInterface,
)
from epidemicalk.repositories.user import UserRepository, UserRepositoryInterface

__all__ = [
    "DepartmentRepository",
    "DepartmentRepositoryInterface",
    "DistrictRepository",
    "DistrictRepositoryInterface",
    "ProvinceRepository",
    "ProvinceRepositoryInterface",
    "UserRepository",
    "UserRepositoryInterface",
    "bind_repositories",
]


def bind_repositories(binder: Binder) -> Binder:
    binder.bind(UserRepositoryInterface, UserRepository)
    binder.bind(DepartmentRepositoryInterface, DepartmentRepository)
    binder.bind(ProvinceRepositoryInterface, ProvinceRepository)
    binder.bind(DistrictRepositoryInterface, DistrictRepository)
    return binder
