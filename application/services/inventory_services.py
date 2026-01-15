from application.models import db, StockTransaction, Inventory 
from flask import abort

class InventoryService:
    @staticmethod
    def adjust_stock(product_id, location_id, user_id, quantity_delta, tx_type, note=None):

        inventory = db.session.execute(
            db.select(Inventory).filter_by(
                product_id=product_id,
                location_id=location_id
            )
        ).scalar_one_or_none()

        if inventory is None:
            inventory = Inventory(
                product_id=product_id,
                location_id=location_id,
                quantity=0  # start at 0
            )
            db.session.add(inventory)
            db.session.flush()

        inventory.quantity += quantity_delta

        transaction = StockTransaction(
            product_id=product_id,
            location_id=location_id,
            user_id=user_id,
            quantity_delta=quantity_delta,
            transaction_type=tx_type,
            note=note
        )

        db.session.add(transaction)
        db.session.commit()

        return transaction
