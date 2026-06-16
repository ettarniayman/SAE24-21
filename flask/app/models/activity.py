from ..extensions import db


class ActivityCategory(db.Model):
    __tablename__ = "activity_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(20))

    activities = db.relationship("Activity", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<ActivityCategory {self.name_fr}>"


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("activity_categories.id"))

    name_fr = db.Column(db.String(150), nullable=False)
    name_en = db.Column(db.String(150), nullable=False)
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)

    duration_hours = db.Column(db.Numeric(5, 1))
    difficulty = db.Column(db.String(20), default="easy")
    min_age = db.Column(db.Integer)
    max_participants = db.Column(db.Integer)
    price_per_person = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(5), default="EUR")

    image = db.Column(db.String(255))
    video_url = db.Column(db.String(500))
    location_name = db.Column(db.String(150))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))

    includes_fr = db.Column(db.Text)
    includes_en = db.Column(db.Text)
    excludes_fr = db.Column(db.Text)
    excludes_en = db.Column(db.Text)

    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # Types spéciaux
    activity_type = db.Column(db.String(30))
    # types: monument, stadium, museum, medina, desert, mountain, hike,
    #        beach, surf, nautical, family, sport, cultural, luxury, excursion

    def __repr__(self):
        return f"<Activity {self.name_fr}>"
