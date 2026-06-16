from datetime import datetime, timezone
import secrets
from ..extensions import db


class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(80))
    lang = db.Column(db.String(5), default="fr")
    is_active = db.Column(db.Boolean, default=True)
    confirmation_token = db.Column(db.String(100), unique=True)
    is_confirmed = db.Column(db.Boolean, default=False)
    unsubscribe_token = db.Column(db.String(100), unique=True)
    subscribed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    unsubscribed_at = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.confirmation_token = secrets.token_urlsafe(32)
        self.unsubscribe_token = secrets.token_urlsafe(32)

    def __repr__(self):
        return f"<NewsletterSubscriber {self.email}>"
