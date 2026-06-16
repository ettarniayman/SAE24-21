from datetime import datetime, timezone
import secrets
from ..extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    program_id = db.Column(db.Integer, db.ForeignKey("travel_programs.id"))

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    nationality = db.Column(db.String(80))

    participants = db.Column(db.Integer, default=1)
    departure_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    total_price = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(5), default="EUR")

    special_requests = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")
    # statuses: pending, confirmed, cancelled, completed

    payment_status = db.Column(db.String(20), default="unpaid")
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reference = "RTV" + secrets.token_hex(4).upper()

    def __repr__(self):
        return f"<Booking {self.reference}>"
