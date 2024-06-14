from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from config.database import Base


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    image_path: Mapped[str] = mapped_column()

