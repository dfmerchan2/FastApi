from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from config.database import Base


class ProductStore(Base):

    __tablename__ = "product_store"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    availability_qty: Mapped[int] = mapped_column()
    booked_qty: Mapped[int] = mapped_column()
    sold_qty: Mapped[int] = mapped_column()

    product = relationship("Product", foreign_keys=[product_id], backref="product_store")

