from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from core.models.role_model import Role
from config.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.id), nullable=False)
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    role = relationship(Role, foreign_keys=Role.id, backref="users", primaryjoin="User.id==Role.id")




