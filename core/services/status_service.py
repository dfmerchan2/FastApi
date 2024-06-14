from core.models.status_model import Status

class StatusService:

    def __init__(self, db) -> None:
        self.db = db

    def add_status(self, data_status):
        with self.db:
            self.db.add(data_status)
            self.db.commit()

    def get_status_by_name(self, status_name):
        with self.db:
            role = self.db.query(Status).filter(Status.name == status_name).first()
            return role
