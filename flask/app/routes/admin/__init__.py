from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from functools import wraps
from ...extensions import db
from ...models.destination import Destination
from ...models.program import TravelProgram
from ...models.hotel import Hotel
from ...models.booking import Booking
from ...models.user import User
from ...models.contact import ContactMessage
from ...models.testimonial import Testimonial
from ...models.newsletter import NewsletterSubscriber

bp = Blueprint("admin", __name__)


@bp.context_processor
def inject_pending_orders_count():
    from ...models.order import Order
    if not current_user.is_authenticated:
        return {}
    return {"pending_orders_count": Order.query.filter_by(status="pending").count()}


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        from flask import redirect, url_for, flash
        if not current_user.is_agent():
            flash("Accès refusé.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


def super_admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        from flask import redirect, url_for, flash
        if not current_user.is_admin():
            flash("Accès réservé aux administrateurs.", "danger")
            return redirect(url_for("admin.dashboard"))
        return f(*args, **kwargs)
    return decorated


# ─── Dashboard ───────────────────────────────────────────────────────────────

@bp.route("/")
@admin_required
def dashboard():
    from ...models.order import Order

    stats = {
        "destinations": Destination.query.count(),
        "programs": TravelProgram.query.count(),
        "hotels": Hotel.query.count(),
        "bookings": Booking.query.count(),
        "orders": Order.query.count(),
        "orders_pending": Order.query.filter_by(status="pending").count(),
        "users": User.query.count(),
        "messages": ContactMessage.query.filter_by(is_read=False).count(),
        "testimonials_pending": Testimonial.query.filter_by(is_approved=False).count(),
        "newsletter": NewsletterSubscriber.query.filter_by(is_active=True).count(),
    }
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    pending_testimonials = Testimonial.query.filter_by(is_approved=False).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_bookings=recent_bookings,
        recent_orders=recent_orders,
        recent_messages=recent_messages,
        pending_testimonials=pending_testimonials,
    )


# Les modules ci-dessous enregistrent leurs routes sur `bp` au moment de l'import.
from . import destinations  # noqa: E402,F401
from . import hotels  # noqa: E402,F401
from . import countries  # noqa: E402,F401
from . import airlines  # noqa: E402,F401
from . import shop  # noqa: E402,F401
from . import programs  # noqa: E402,F401
from . import blog  # noqa: E402,F401
from . import users  # noqa: E402,F401
from . import testimonials  # noqa: E402,F401
from . import promotions  # noqa: E402,F401
from . import messages  # noqa: E402,F401
from . import faq  # noqa: E402,F401
from . import rss  # noqa: E402,F401
from . import media  # noqa: E402,F401
from . import newsletter  # noqa: E402,F401
from . import bookings  # noqa: E402,F401
from . import orders  # noqa: E402,F401
from . import reports  # noqa: E402,F401
