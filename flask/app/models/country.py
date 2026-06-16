from ..extensions import db


class Country(db.Model):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)
    continent = db.Column(db.String(50))
    capital = db.Column(db.String(100))
    currency = db.Column(db.String(50))
    currency_code = db.Column(db.String(10))
    language = db.Column(db.String(100))
    flag_emoji = db.Column(db.String(10))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    destinations = db.relationship("Destination", backref="country", lazy="dynamic")

    def __repr__(self):
        return f"<Country {self.name_fr}>"
