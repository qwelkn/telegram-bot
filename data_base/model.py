from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.types import BigInteger

class Base(DeclarativeBase):
    pass

class Bag(Base):
    __tablename__ = "user_bag"
    id: Mapped[int] = mapped_column(primary_key=True)
    protection: Mapped[int]
    docs: Mapped[int]
    taxi: Mapped[int]
    mina: Mapped[int]

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    fullname: Mapped[str] = mapped_column(String(127))
    coins: Mapped[int] 
    diamonts: Mapped[int]
    bag_id: Mapped[int] = mapped_column(ForeignKey("user_bag.id")) 
    play_game: Mapped[int]
    win_game: Mapped[int]
    los_game: Mapped[int]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)

class UserGroup(Base):
    __tablename__ = "user-group"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("user_acount"))
    group: Mapped[int] = mapped_column(ForeignKey("groups"))

class Achive(Base):
    __tablename__ = "achive"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127))
    task: Mapped[str]

class UserAchive(Base):
    __tablename__ = "user-achive"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("user_acount"))
    achive: Mapped[int] = mapped_column(ForeignKey("achive"))

# class Address(Base):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"