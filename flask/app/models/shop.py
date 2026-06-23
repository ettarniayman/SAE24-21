from datetime import datetime, timezone
from ..extensions import db


class ShopCategory(db.Model):
    __tablename__ = "shop_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    products = db.relationship("ShopProduct", backref="category", lazy="dynamic")


class ShopProduct(db.Model):
    __tablename__ = "shop_products"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("shop_categories.id"))

    name_fr = db.Column(db.String(150), nullable=False)
    name_en = db.Column(db.String(150))
    description_fr = db.Column(db.Text)
    description_en = db.Column(db.Text)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    price_discounted = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(5), default="EUR")

    image_main = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True)

    brand = db.Column(db.String(100))
    affiliate_url = db.Column(db.String(500))
    is_affiliate = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    rating = db.Column(db.Numeric(3, 1))
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    medias = db.relationship("Media", backref="product", lazy="dynamic", foreign_keys="Media.product_id")

    def __repr__(self):
        return f"<ShopProduct {self.name_fr}>"


class ShopOrder(db.Model):
    __tablename__ = "shop_orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("shop_products.id"))
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Numeric(10, 2))
    total_price = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
