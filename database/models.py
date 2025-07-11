from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(String(127))
    coins: Mapped[int] = mapped_column(default=0)
    diamonds: Mapped[int] = mapped_column(default=0)
    games_played: Mapped[int] = mapped_column(default=0)
    games_won: Mapped[int] = mapped_column(default=0)
    games_lost: Mapped[int] = mapped_column(default=0)

    bag = relationship("Bag", back_populates="user", uselist=False)
    achievements = relationship("UserAchievement", back_populates="user")
    groups = relationship("UserGroup", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, tg_id={self.tg_id!r}, fullname={self.fullname!r})"


class Bag(Base):
    __tablename__ = "bags"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    protection: Mapped[int] = mapped_column(default=0)
    docs: Mapped[int] = mapped_column(default=0)
    taxi: Mapped[int] = mapped_column(default=0)
    mina: Mapped[int] = mapped_column(default=0)

    user = relationship("User", back_populates="bag")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    members = relationship("UserGroup", back_populates="group")


class UserGroup(Base):
    __tablename__ = "user_groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="members")


class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127))
    description: Mapped[str] = mapped_column(String(255))
    cost: Mapped[int] = mapped_column(default=0)

    users = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")
