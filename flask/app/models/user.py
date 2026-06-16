from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default="client")
    # roles: super_admin, admin, agent, client
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    avatar = db.Column(db.String(255))
    preferred_lang = db.Column(db.String(5), default="fr")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

    bookings = db.relationship("Booking", backref="user", lazy="dynamic")
    testimonials = db.relationship("Testimonial", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def is_admin(self):
        return self.role in ("super_admin", "admin")

    def is_super_admin(self):
        return self.role == "super_admin"

    def is_agent(self):
        return self.role in ("super_admin", "admin", "agent")

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
