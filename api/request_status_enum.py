from enum import Enum


class RequestStatusEnum(str, Enum):
    DONE = 'done'
    PENDING = 'pending'
    NOT_FOUND = 'not found'
