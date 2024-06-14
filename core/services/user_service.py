from core.models.user_model import User


class UserService:

    def __init__(self, db) -> None:
        self.db = db

    def get_users(self):
        with self.db:
            result = self.db.query(User).all()
            return result

    def get_user_by_id(self, id_user):
        with self.db:
            result = self.db.query(User).filter(User.id == id_user).first()
            return result

    def create_user(self, data_user: User):
        with self.db:
            self.db.add(data_user)
            self.db.commit()

    def update_user(self, record, user_dto):
        with self.db:
            record.name = user_dto.name
            record.address = user_dto.address
            record.phone = user_dto.phone
            self.db.commit()
            self.db.refresh(record)
            return record

    def delete_user(self, record):
        with self.db:
            self.db.delete(record)
            self.db.commit()
            self.db.refresh(record)


