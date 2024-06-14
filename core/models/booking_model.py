from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from config.database import Base
from core.models.products_model import Product
from core.models.status_model import Status
from core.models.user_model import User


class Booking(Base):

    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    delivery_address: Mapped[str] = mapped_column()
    delivery_date: Mapped[str] = mapped_column()
    delivery_time: Mapped[str] = mapped_column()
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    quantity: Mapped[int] = mapped_column()

    users = relationship(User, foreign_keys=[user_id], backref="booking")
    product = relationship(Product, foreign_keys=[product_id], backref="booking")
    status = relationship(Status, foreign_keys=[status_id], backref="booking")


