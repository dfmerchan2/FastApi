from core.models.product_store_model import ProductStore
from core.models.products_model import Product


class ProductStoreService:

    def __init__(self, db):
        self.db = db

    def get_products_store(self):
        with self.db:
            result = self.db.query(ProductStore).all()
            return result

    def get_product_store_by_id(self, id_product):
        with self.db:
            result = self.db.query(ProductStore).filter(ProductStore.id == id_product).first()
            return result

    def create_product_store(self, data_product: ProductStore):
        with self.db:
            self.db.add(data_product)
            self.db.commit()

    def update_product_store(self, record, product_store_dto):
        with self.db:
            record.available_qty = product_store_dto.available_qty
            record.booked_qty = product_store_dto.booked_qty
            record.sold_qty = product_store_dto.sold_qty
            self.db.commit()
            self.db.refresh(record)
            return record

    def delete_product_store(self, record):
        with self.db:
            self.db.delete(record)
            self.db.commit()
            self.db.refresh(record)
