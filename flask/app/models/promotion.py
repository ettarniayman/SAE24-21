from datetime import datetime, timezone
from ..extensions import db


class Promotion(db.Model):
    __tablename__ = "promotions"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))

    title_fr = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)

    original_price = db.Column(db.Numeric(10, 2))
    promo_price = db.Column(db.Numeric(10, 2))
    discount_percent = db.Column(db.Integer)
    currency = db.Column(db.String(5), default="EUR")

    promo_code = db.Column(db.String(30))
    image = db.Column(db.String(255))

    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    promo_type = db.Column(db.String(30), default="general")
    # types: general, flight, hotel, package, activity

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def is_valid(self):
        now = datetime.now(timezone.utc)
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return self.is_active

    def __repr__(self):
        return f"<Promotion {self.title_fr}>"
