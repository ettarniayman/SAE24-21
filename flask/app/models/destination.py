from datetime import datetime, timezone
from ..extensions import db

destination_activities = db.Table(
    "destination_activities",
    db.Column("destination_id", db.Integer, db.ForeignKey("destinations.id"), primary_key=True),
    db.Column("activity_id", db.Integer, db.ForeignKey("activities.id"), primary_key=True),
    db.Column("sort_order", db.Integer, default=0),
)

destination_themes = db.Table(
    "destination_themes",
    db.Column("destination_id", db.Integer, db.ForeignKey("destinations.id"), primary_key=True),
    db.Column("theme", db.String(50), primary_key=True),
)


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    region = db.Column(db.String(100))

    name_fr = db.Column(db.String(120), nullable=False)
    name_en = db.Column(db.String(120), nullable=False)
    short_desc_fr = db.Column(db.String(500))
    short_desc_en = db.Column(db.String(500))
    long_desc_fr = db.Column(db.Text)
    long_desc_en = db.Column(db.Text)
    history_fr = db.Column(db.Text)
    history_en = db.Column(db.Text)
    culture_fr = db.Column(db.Text)
    culture_en = db.Column(db.Text)
    gastronomy_fr = db.Column(db.Text)
    gastronomy_en = db.Column(db.Text)

    # Geography
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))
    timezone_name = db.Column(db.String(50))
    altitude_m = db.Column(db.Integer)

    # Climate
    climate_fr = db.Column(db.Text)
    climate_en = db.Column(db.Text)
    best_period_fr = db.Column(db.String(200))
    best_period_en = db.Column(db.String(200))
    avg_temp_jan = db.Column(db.Integer)
    avg_temp_jul = db.Column(db.Integer)

    # Practical info
    average_budget_eur = db.Column(db.Integer)
    budget_low = db.Column(db.Numeric(10, 2))
    budget_high = db.Column(db.Numeric(10, 2))
    currency_local = db.Column(db.String(30))
    difficulty_level = db.Column(db.String(20), default="easy")
    safety_level = db.Column(db.String(20), default="safe")
    visa_required = db.Column(db.Boolean, default=False)
    visa_info_fr = db.Column(db.Text)

    # Media
    image_main = db.Column(db.String(255))
    image_thumb = db.Column(db.String(255))
    video_url = db.Column(db.String(500))
    video_drone_url = db.Column(db.String(500))
    youtube_id = db.Column(db.String(50))
    vimeo_id = db.Column(db.String(50))
    street_view_lat = db.Column(db.Numeric(10, 7))
    street_view_lng = db.Column(db.Numeric(10, 7))

    # SEO
    meta_title_fr = db.Column(db.String(200))
    meta_title_en = db.Column(db.String(200))
    meta_desc_fr = db.Column(db.String(300))
    meta_desc_en = db.Column(db.String(300))

    # Status & stats
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    destination_type = db.Column(db.String(30), default="city")
    # types: city, nature, desert, mountain, beach, historical

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    activities = db.relationship("Activity", secondary=destination_activities, backref="destinations", lazy="dynamic")
    medias = db.relationship("Media", backref="destination", lazy="dynamic", foreign_keys="Media.destination_id")
    testimonials = db.relationship("Testimonial", backref="destination", lazy="dynamic")
    hotels = db.relationship("Hotel", backref="destination", lazy="dynamic")
    programs = db.relationship("TravelProgram", secondary="program_destinations", backref="destinations")
    promotions = db.relationship("Promotion", backref="destination", lazy="dynamic")

    def get_name(self, lang="fr"):
        return self.name_fr if lang == "fr" else self.name_en

    def get_short_desc(self, lang="fr"):
        return self.short_desc_fr if lang == "fr" else self.short_desc_en

    def get_long_desc(self, lang="fr"):
        return self.long_desc_fr if lang == "fr" else self.long_desc_en

    @property
    def avg_rating(self):
        from .testimonial import Testimonial
        reviews = Testimonial.query.filter_by(destination_id=self.id, is_approved=True).all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        from .testimonial import Testimonial
        return Testimonial.query.filter_by(destination_id=self.id, is_approved=True).count()

    def __repr__(self):
        return f"<Destination {self.name_fr}>"
