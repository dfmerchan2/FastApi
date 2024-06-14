from core.models.booking_model import Booking
from core.models.products_model import Product
from core.models.status_model import Status
from core.models.user_model import User


class BookingService:

    def __init__(self, db) -> None:
        self.db = db

    def get_booking(self):
        with self.db:
            result = self.db.query(Booking).all()
            return result

    def get_booking_by_id(self, id_booking):
        with self.db:
            result = self.db.query(Booking).filter(Booking.id == id_booking).first()
            return result

    def get_booking_by_user(self, user_id):
        with self.db:
            result = self.db.query(Booking).filter(Booking.user_id == user_id).all()
            return result

    def get_user_info(self, user_email):
        with self.db:
            result = self.db.query(User).outerjoin(Booking).filter(User.email == user_email).first()
            return result

    def get_product_info(self, product_name):
        with self.db:
            result = self.db.query(Product).outerjoin(Booking).filter(Product.name.ilike(product_name)).first()
            return result

    def get_status_name(self, status_name):
        with self.db:
            result = self.db.query(Status).filter(Status.name == status_name).first()
            return result

    def create_booking(self, data_booking: Booking):
        with self.db:
            self.db.add(data_booking)
            self.db.commit()

    def update_booking(self, record, booking):
        with self.db:
            record.date = booking["date"]
            record.time = booking["time"]
            record.status_id = booking["status_id"]
            record.quantity = booking["quantity"]
            self.db.commit()
            self.db.refresh(record)
            return record

    def delete_booking(self, record):
        with self.db:
            self.db.delete(record)
            self.db.commit()
            self.db.refresh(record)
