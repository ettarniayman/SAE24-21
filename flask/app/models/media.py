from datetime import datetime, timezone
from ..extensions import db


class Media(db.Model):
    __tablename__ = "medias"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"))

    filename = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255))
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20))  # image, video, pdf
    mime_type = db.Column(db.String(80))
    file_size = db.Column(db.Integer)

    title_fr = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    alt_fr = db.Column(db.String(200))
    caption_fr = db.Column(db.Text)

    media_category = db.Column(db.String(30), default="gallery")
    # categories: main, gallery, drone, immersive, ai_generated, document

    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Media {self.filename}>"
