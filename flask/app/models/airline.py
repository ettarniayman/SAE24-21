from datetime import datetime, timezone
from ..extensions import db


class Airline(db.Model):
    __tablename__ = "airlines"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    iata_code = db.Column(db.String(5))
    country_code = db.Column(db.String(5))
    logo = db.Column(db.String(255))
    website = db.Column(db.String(300))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)
    alliance = db.Column(db.String(50))

    baggage_cabin_kg = db.Column(db.Integer)
    baggage_hold_kg = db.Column(db.Integer)
    baggage_policy_fr = db.Column(db.Text)

    has_business_class = db.Column(db.Boolean, default=True)
    has_first_class = db.Column(db.Boolean, default=False)
    is_partner = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)

    promotions = db.relationship("FlightPromotion", backref="airline", lazy="dynamic")

    def __repr__(self):
        return f"<Airline {self.name}>"


class FlightPromotion(db.Model):
    __tablename__ = "flight_promotions"

    id = db.Column(db.Integer, primary_key=True)
    airline_id = db.Column(db.Integer, db.ForeignKey("airlines.id"), nullable=False)

    title_fr = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    description_fr = db.Column(db.Text)
    origin = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    origin_iata = db.Column(db.String(5))
    destination_iata = db.Column(db.String(5))
    price_from = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(5), default="EUR")
    valid_from = db.Column(db.Date)
    valid_until = db.Column(db.Date)
    booking_url = db.Column(db.String(500))
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<FlightPromotion {self.title_fr}>"
