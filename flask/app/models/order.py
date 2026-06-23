from datetime import datetime, timezone
import secrets
from ..extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    billing_address = db.Column(db.Text)

    status = db.Column(db.String(20), nullable=False, default="pending")
    # statuses: pending, confirmed, paid, processing, completed, cancelled, refunded
    payment_status = db.Column(db.String(20), nullable=False, default="pending")

    subtotal = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    currency = db.Column(db.String(3), nullable=False, default="EUR")

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    items = db.relationship("OrderItem", backref="order", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.reference:
            year = datetime.now(timezone.utc).year
            self.reference = f"RTV-{year}-{secrets.token_hex(3).upper()}"
            # Format RTV-<annee>-<hex aleatoire>, coherent avec Booking.reference
            # (RTV + hex) plutot qu'un compteur sequentiel pour eviter toute
            # race condition d'unicite sous ecriture concurrente.

    def __repr__(self):
        return f"<Order {self.reference}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    # item_type: program, product
    program_id = db.Column(db.Integer, db.ForeignKey("travel_programs.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("shop_products.id"))

    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    departure_date = db.Column(db.Date)
    participants = db.Column(db.Integer)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)

    program = db.relationship("TravelProgram")
    product = db.relationship("ShopProduct")

    def __repr__(self):
        return f"<OrderItem {self.item_type} order={self.order_id}>"
