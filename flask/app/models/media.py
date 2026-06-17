import re
from datetime import datetime, timezone
from ..extensions import db


class Media(db.Model):
    __tablename__ = "medias"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"))
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"))

    filename = db.Column(db.String(255), nullable=True)   # nullable when video_url is used
    original_name = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(20))  # image, video, pdf
    mime_type = db.Column(db.String(80))
    file_size = db.Column(db.Integer)      # bytes
    file_size_kb = db.Column(db.Integer)   # kilobytes (for display)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    title_fr = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    alt_fr = db.Column(db.String(200))
    alt_text = db.Column(db.String(200))   # legacy compat with schema.sql
    caption_fr = db.Column(db.Text)

    video_url = db.Column(db.String(500))        # external YouTube/Vimeo URL
    duration_seconds = db.Column(db.Integer)

    media_category = db.Column(db.String(30), default="gallery")
    # categories: main, gallery, drone, immersive, ai_generated, document

    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def youtube_id(self):
        if not self.video_url:
            return None
        m = re.search(
            r'(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([a-zA-Z0-9_-]{11})',
            self.video_url
        )
        return m.group(1) if m else None

    @property
    def is_youtube(self):
        return bool(self.video_url and ('youtube.com' in self.video_url or 'youtu.be' in self.video_url))

    @property
    def is_vimeo(self):
        return bool(self.video_url and 'vimeo.com' in self.video_url)

    def __repr__(self):
        return f"<Media {self.filename or self.video_url}>"
