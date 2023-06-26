import enum


class RequestStatusEnum(str, enum.Enum):
    DONE = 'done'
    PENDING = 'pending'
    PROCESSED = 'processed'
    NOT_FOUND = 'not found'
