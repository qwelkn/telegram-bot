from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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
    cost: Mapped[int]


class UserAchive(Base):
    __tablename__ = "user-achive"
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("user_acount"))
    achive: Mapped[int] = mapped_column(ForeignKey("achive"))


class Profile(Base):
    __tablename__ = "user-achive"
    play_game: Mapped[int]
    win_game: Mapped[int]
    task_completed: Mapped[int]
    achive: Mapped[str]
    rank: Mapped[str]
