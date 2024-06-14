from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from config.database import Base


class Role(Base):

    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

