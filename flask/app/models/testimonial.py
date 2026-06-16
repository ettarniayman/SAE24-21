from datetime import datetime, timezone
from ..extensions import db


class Testimonial(db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    program_id = db.Column(db.Integer, db.ForeignKey("travel_programs.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    client_name = db.Column(db.String(100), nullable=False)
    client_country = db.Column(db.String(80))
    client_photo = db.Column(db.String(255))
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200))
    comment = db.Column(db.Text, nullable=False)
    travel_date = db.Column(db.Date)
    is_approved = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Testimonial {self.client_name} {self.rating}/5>"
