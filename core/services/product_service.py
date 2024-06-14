from core.models.products_model import Product


class ProductService:

    def __init__(self, db) -> None:
        self.db = db

    def get_product(self):
        with self.db:
            result = self.db.query(Product).all()
            return result

    def get_product_by_id(self, product_id):
        with self.db:
            result = self.db.query(Product).filter(Product.id == product_id).first()
            return result

    def get_product_by_name(self, product_name):
        with self.db:
            result = self.db.query(Product).filter(Product.name.ilike(product_name)).first()
            return result

    def create_product(self, data_product: Product):
        with self.db:
            self.db.add(data_product)
            self.db.commit()

    def update_product(self, record, product_dto):
        with self.db:
            record.name = product_dto.name
            record.description = product_dto.description
            record.author = product_dto.author
            record.price = product_dto.price
            record.image_path = product_dto.image_path
            self.db.commit()
            self.db.refresh(record)
            return record

    def delete_product(self, record):
        with self.db:
            self.db.delete(record)
            self.db.commit()
            self.db.refresh(record)
