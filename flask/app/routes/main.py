from flask import Blueprint, render_template, request, redirect, url_for, make_response
from ..models.destination import Destination
from ..models.program import TravelProgram
from ..models.testimonial import Testimonial
from ..models.promotion import Promotion
from ..models.blog import BlogPost
from ..models.airline import Airline
from ..extensions import db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    featured_destinations = Destination.query.filter_by(is_featured=True, is_active=True).limit(8).all()
    popular_programs = TravelProgram.query.filter_by(is_featured=True, is_active=True).limit(6).all()
    featured_testimonials = Testimonial.query.filter_by(is_approved=True, is_featured=True).limit(6).all()
    active_promotions = Promotion.query.filter_by(is_active=True, is_featured=True).limit(4).all()
    recent_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).limit(3).all()
    airlines = Airline.query.filter_by(is_partner=True, is_active=True).limit(8).all()

    stats = {
        "destinations": Destination.query.filter_by(is_active=True).count(),
        "programs": TravelProgram.query.filter_by(is_active=True).count(),
        "travelers": 15000,
        "countries": 45,
    }

    return render_template(
        "index.html",
        featured_destinations=featured_destinations,
        popular_programs=popular_programs,
        featured_testimonials=featured_testimonials,
        active_promotions=active_promotions,
        recent_posts=recent_posts,
        airlines=airlines,
        stats=stats,
    )


@bp.route("/set-lang/<lang>")
def set_lang(lang):
    if lang not in ("fr", "en"):
        lang = "fr"
    referer = request.referrer or url_for("main.index")
    resp = make_response(redirect(referer))
    resp.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365)
    return resp


@bp.route("/a-propos")
def about():
    return render_template("pages/about.html")


@bp.route("/mentions-legales")
def legal():
    return render_template("pages/legal.html")


@bp.route("/politique-de-confidentialite")
def privacy():
    return render_template("pages/privacy.html")


@bp.route("/conditions-generales")
def terms():
    return render_template("pages/terms.html")


@bp.route("/faq")
def faq():
    from ..models.faq import FAQCategory
    categories = FAQCategory.query.order_by(FAQCategory.order).all()
    return render_template("pages/faq.html", categories=categories)


@bp.route("/sitemap.xml")
def sitemap():
    from ..utils.helpers import generate_sitemap
    content = generate_sitemap()
    resp = make_response(content)
    resp.headers["Content-Type"] = "application/xml"
    return resp


@bp.route("/robots.txt")
def robots():
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /auth/\nSitemap: /sitemap.xml\n"
    resp = make_response(content)
    resp.headers["Content-Type"] = "text/plain"
    return resp


@bp.route("/newsletter/subscribe", methods=["POST"])
def newsletter_subscribe():
    from ..models.newsletter import NewsletterSubscriber
    from ..forms.newsletter_forms import NewsletterForm
    form = NewsletterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        existing = NewsletterSubscriber.query.filter_by(email=email).first()
        if not existing:
            sub = NewsletterSubscriber(email=email, first_name=form.first_name.data)
            db.session.add(sub)
            db.session.commit()
    return redirect(request.referrer or url_for("main.index"))
