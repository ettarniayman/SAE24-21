from datetime import datetime, timezone
from ..extensions import db

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("blog_posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("blog_tags.id"), primary_key=True),
)


class BlogCategory(db.Model):
    __tablename__ = "blog_categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name_fr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_fr = db.Column(db.Text)
    color = db.Column(db.String(20))
    icon = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    posts = db.relationship("BlogPost", backref="category", lazy="dynamic")


class BlogTag(db.Model):
    __tablename__ = "blog_tags"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("blog_categories.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    title_fr = db.Column(db.String(250), nullable=False)
    title_en = db.Column(db.String(250))
    excerpt_fr = db.Column(db.Text)
    excerpt_en = db.Column(db.Text)
    content_fr = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text)

    image_main = db.Column(db.String(255))
    image_alt_fr = db.Column(db.String(200))

    meta_title_fr = db.Column(db.String(200))
    meta_desc_fr = db.Column(db.String(300))

    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)

    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    tags = db.relationship("BlogTag", secondary=post_tags, backref="posts", lazy="dynamic")
    author = db.relationship("User", backref="blog_posts", foreign_keys=[author_id])
    medias = db.relationship("Media", backref="post", lazy="dynamic", foreign_keys="Media.post_id")

    def publish(self):
        self.is_published = True
        self.published_at = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<BlogPost {self.title_fr[:50]}>"
