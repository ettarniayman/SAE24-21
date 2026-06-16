from datetime import datetime, timezone
from ..extensions import db


class RSSItem(db.Model):
    __tablename__ = "rss_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(500))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    # categories: news, destination, promotion, article, partner
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    published_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<RSSItem {self.title[:60]}>"
