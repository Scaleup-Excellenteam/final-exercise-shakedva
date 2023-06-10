from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: list
    is_done: bool = field(init=False)
    not_found: bool = field(init=False)

    def __post_init__(self):
        self.is_done = (self.status == 'done')
        self.not_found = (self.status == 'not found')

    def __bool__(self) -> bool:
        return self.is_done
