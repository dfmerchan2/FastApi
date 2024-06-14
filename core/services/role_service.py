from core.models.role_model import Role


class RoleService:

    def __init__(self, db) -> None:
        self.db = db

    def add_roles(self, data_role):
        with self.db:
            self.db.add(data_role)
            self.db.commit()

    def get_role_by_id(self, id_role):
        with self.db:
            role = self.db.query(Role).filter(Role.id == id_role).first()
            return role

    def get_role_by_name(self, role_name):
        with self.db:
            role = self.db.query(Role).filter(Role.name == role_name).first()
            return role

