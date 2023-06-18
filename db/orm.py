import uuid

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey

from typing import List
from sqlalchemy import Integer, String, UUID, DateTime
from sqlalchemy import create_engine
import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String)

    # todo?
    uploads: Mapped[List["Upload"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Upload(Base):
    __tablename__ = "upload"

    id = mapped_column(Integer, primary_key=True)
    uid = mapped_column(String)  # TODO
    filename = mapped_column(String)
    upload_time = mapped_column(DateTime)
    finish_time = mapped_column(DateTime)
    status = mapped_column(String)
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="uploads")


engine = create_engine(
    "sqlite:///C:\\Users\\shake\\Desktop\\College\\4th Year\\Semester B\\Excellenteam\\python\\Ex\\final-exercise-shakedva\\db\\example.db")
# engine = create_engine("sqlite:////example.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session

user1 = User(email="someuser@gmail.com")
upload1 = Upload(
    uid=str(uuid.uuid1()),  # TODO
    filename="file_name_test",
    upload_time=datetime.datetime.now(),
    finish_time=datetime.datetime.now(),
    status='done',
    user_id=user1.id,
    user=user1
)
user1.uploads.append(upload1)
# session.add(user1)
# session.add(upload1)
# session.commit()
