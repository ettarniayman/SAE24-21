from datetime import datetime, timezone
from ..extensions import db


class Hotel(db.Model):
    __tablename__ = "hotels"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    hotel_type = db.Column(db.String(30), default="hotel")
    # types: hotel, riad, villa, resort, hostel, apartment

    stars = db.Column(db.Integer)
    address = db.Column(db.String(300))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(150))
    website = db.Column(db.String(255))

    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)

    price_min = db.Column(db.Numeric(10, 2))
    price_max = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(5), default="EUR")

    image_main = db.Column(db.String(255))
    amenities = db.Column(db.Text)  # JSON string of amenities
    check_in_time = db.Column(db.String(10))
    check_out_time = db.Column(db.String(10))

    has_pool = db.Column(db.Boolean, default=False)
    has_spa = db.Column(db.Boolean, default=False)
    has_restaurant = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=True)
    has_parking = db.Column(db.Boolean, default=False)
    has_gym = db.Column(db.Boolean, default=False)
    has_bar = db.Column(db.Boolean, default=False)
    has_beach_access = db.Column(db.Boolean, default=False)

    rating = db.Column(db.Numeric(3, 1))
    review_count = db.Column(db.Integer, default=0)

    booking_url = db.Column(db.String(500))
    is_partner = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    medias = db.relationship("Media", backref="hotel", lazy="dynamic", foreign_keys="Media.hotel_id")

    def __repr__(self):
        return f"<Hotel {self.name}>"
