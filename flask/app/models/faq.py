from ..extensions import db


class FAQCategory(db.Model):
    __tablename__ = "faq_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    order = db.Column(db.Integer, default=0)

    items = db.relationship("FAQItem", backref="category", lazy="dynamic", order_by="FAQItem.order")


class FAQItem(db.Model):
    __tablename__ = "faq_items"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("faq_categories.id"))
    question_fr = db.Column(db.Text, nullable=False)
    question_en = db.Column(db.Text)
    answer_fr = db.Column(db.Text, nullable=False)
    answer_en = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<FAQItem {self.question_fr[:50]}>"
