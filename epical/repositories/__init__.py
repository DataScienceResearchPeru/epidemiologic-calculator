from injector import Binder

from epical.repositories.department import (
    DepartmentRepository,
    DepartmentRepositoryInterface,
)
from epical.repositories.district import DistrictRepository, DistrictRepositoryInterface
from epical.repositories.province import ProvinceRepository, ProvinceRepositoryInterface
from epical.repositories.user import UserRepository, UserRepositoryInterface

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
