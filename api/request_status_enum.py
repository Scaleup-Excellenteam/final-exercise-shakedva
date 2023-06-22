import enum


# class RequestStatusEnum(str, Enum):
class RequestStatusEnum(str, enum.Enum):
    DONE = 'done'
    PENDING = 'pending'
    NOT_FOUND = 'not found'
