from enum import Enum


class RolesEnum(Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    CUSTOMER = "CUSTOMER"


class StatusEnum(Enum):
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    IN_DELIVERY = "IN_DELIVERY"
