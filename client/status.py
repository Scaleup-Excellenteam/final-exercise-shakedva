from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Status:
    """
    Status contains the information of the output request
    """
    status: str
    filename: str
    timestamp: datetime
    explanation: list
    is_done: bool = field(init=False)
    not_found: bool = field(init=False)

    def __post_init__(self):
        """
        Post initialization of non constructor class members.
        """
        self.is_done = (self.status == 'done')
        self.not_found = (self.status == 'not found')

    def __bool__(self) -> bool:
        """
        Evaluate the Status class to True if the status is done, False otherwise.
        :return:
        """
        return self.is_done
