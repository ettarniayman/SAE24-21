from flask import Blueprint, render_template, request, abort, jsonify
from ..models.destination import Destination
from ..models.activity import ActivityCategory
from ..models.testimonial import Testimonial
from ..models.hotel import Hotel
from ..models.program import TravelProgram
from ..models.country import Country
from ..extensions import db
from sqlalchemy import or_

bp = Blueprint("destinations", __name__)


@bp.route("/")
def list_destinations():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "")
    country_id = request.args.get("country", type=int)
    dest_type = request.args.get("type", "")
    theme = request.args.get("theme", "")
    sort = request.args.get("sort", "featured")

    query = Destination.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            or_(
                Destination.name_fr.ilike(f"%{search}%"),
                Destination.name_en.ilike(f"%{search}%"),
                Destination.short_desc_fr.ilike(f"%{search}%"),
            )
        )
    if country_id:
        query = query.filter_by(country_id=country_id)
    if dest_type:
        query = query.filter_by(destination_type=dest_type)

    if sort == "popular":
        query = query.order_by(Destination.view_count.desc())
    elif sort == "budget":
        query = query.order_by(Destination.average_budget_eur.asc())
    else:
        query = query.order_by(Destination.is_featured.desc(), Destination.view_count.desc())

    pagination = query.paginate(page=page, per_page=12, error_out=False)
    countries = Country.query.filter_by(is_active=True).order_by(Country.name_fr).all()

    return render_template(
        "destinations/list.html",
        destinations=pagination.items,
        pagination=pagination,
        countries=countries,
        search=search,
        current_country=country_id,
        current_type=dest_type,
        current_sort=sort,
    )


@bp.route("/<slug>")
def detail(slug):
    dest = Destination.query.filter_by(slug=slug, is_active=True).first_or_404()
    dest.view_count = (dest.view_count or 0) + 1
    db.session.commit()

    testimonials = Testimonial.query.filter_by(
        destination_id=dest.id, is_approved=True
    ).order_by(Testimonial.created_at.desc()).limit(6).all()

    hotels = Hotel.query.filter_by(
        destination_id=dest.id, is_active=True
    ).order_by(Hotel.stars.desc()).limit(6).all()

    programs = (
        TravelProgram.query
        .filter(TravelProgram.destinations.any(id=dest.id), TravelProgram.is_active == True)
        .limit(4).all()
    )

    related = (
        Destination.query
        .filter(Destination.country_id == dest.country_id, Destination.id != dest.id, Destination.is_active == True)
        .limit(4).all()
    )

    activities = list(dest.activities.filter_by(is_active=True).all())
    medias = list(dest.medias.filter_by(is_active=True).order_by("sort_order").all())

    return render_template(
        "destinations/detail.html",
        dest=dest,
        testimonials=testimonials,
        hotels=hotels,
        programs=programs,
        related=related,
        activities=activities,
        medias=medias,
    )


@bp.route("/pays/<code>")
def by_country(code):
    country = Country.query.filter_by(code=code.upper(), is_active=True).first_or_404()
    destinations = Destination.query.filter_by(country_id=country.id, is_active=True).all()
    return render_template("destinations/by_country.html", country=country, destinations=destinations)
