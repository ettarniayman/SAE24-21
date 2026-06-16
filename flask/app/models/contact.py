from datetime import datetime, timezone
from ..extensions import db


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    destination_interest = db.Column(db.String(150))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    lang = db.Column(db.String(5), default="fr")
    ip_address = db.Column(db.String(50))
    is_read = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<ContactMessage {self.email} - {self.subject[:40]}>"
