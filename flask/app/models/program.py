from datetime import datetime, timezone
from ..extensions import db

program_destinations = db.Table(
    "program_destinations",
    db.Column("program_id", db.Integer, db.ForeignKey("travel_programs.id"), primary_key=True),
    db.Column("destination_id", db.Integer, db.ForeignKey("destinations.id"), primary_key=True),
)


class TravelProgram(db.Model):
    __tablename__ = "travel_programs"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)

    name_fr = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    tagline_fr = db.Column(db.String(300))
    tagline_en = db.Column(db.String(300))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)

    duration_days = db.Column(db.Integer, nullable=False)
    duration_nights = db.Column(db.Integer)
    group_min = db.Column(db.Integer, default=1)
    group_max = db.Column(db.Integer, default=20)

    price_per_person = db.Column(db.Numeric(10, 2))
    price_per_person_discounted = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(5), default="EUR")

    includes_fr = db.Column(db.Text)
    includes_en = db.Column(db.Text)
    excludes_fr = db.Column(db.Text)
    excludes_en = db.Column(db.Text)

    image_main = db.Column(db.String(255))
    difficulty = db.Column(db.String(20), default="easy")

    theme = db.Column(db.String(50))
    # themes: culture, adventure, nature, luxury, sport, gastronomy, family, football

    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    booking_count = db.Column(db.Integer, default=0)

    departure_city = db.Column(db.String(100))
    departure_country_code = db.Column(db.String(5))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    days = db.relationship("ProgramDay", backref="program", lazy="dynamic", order_by="ProgramDay.day_number")
    bookings = db.relationship("Booking", backref="program", lazy="dynamic")

    def __repr__(self):
        return f"<TravelProgram {self.name_fr}>"


class ProgramDay(db.Model):
    __tablename__ = "program_days"

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey("travel_programs.id"), nullable=False)
    day_number = db.Column(db.Integer, nullable=False)

    title_fr = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)

    morning_fr = db.Column(db.Text)
    morning_en = db.Column(db.Text)
    afternoon_fr = db.Column(db.Text)
    afternoon_en = db.Column(db.Text)
    evening_fr = db.Column(db.Text)
    evening_en = db.Column(db.Text)

    accommodation = db.Column(db.String(200))
    meals_included = db.Column(db.String(20))  # B=Breakfast, L=Lunch, D=Dinner, BLD etc.
    image = db.Column(db.String(255))
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))

    def __repr__(self):
        return f"<ProgramDay {self.program_id} Day {self.day_number}>"
