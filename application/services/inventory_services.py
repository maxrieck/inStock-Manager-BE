from app import StockTransaction, db, Inventory

class InventoryService:
    @staticmethod
    def adjust_stuck(product_id, quanity, tx_type):
        inventory = Inventory.query.filter_by(product_id=product_id).first_or_404()
        inventory.quanity += quanity
        db.session.add(
            StockTransaction(
                product_id=product_id,
                quanity=quanity,
                transaction_type=tx_type
            )
        )
        db.session.commit()                                     
