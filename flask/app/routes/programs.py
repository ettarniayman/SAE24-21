from flask import Blueprint, render_template, request
from ..models.program import TravelProgram
from ..extensions import db

bp = Blueprint("programs", __name__)


@bp.route("/")
def list_programs():
    page = request.args.get("page", 1, type=int)
    theme = request.args.get("theme", "")
    duration = request.args.get("duration", "")
    sort = request.args.get("sort", "featured")

    query = TravelProgram.query.filter_by(is_active=True)
    if theme:
        query = query.filter_by(theme=theme)
    if duration == "short":
        query = query.filter(TravelProgram.duration_days <= 5)
    elif duration == "medium":
        query = query.filter(TravelProgram.duration_days.between(6, 10))
    elif duration == "long":
        query = query.filter(TravelProgram.duration_days > 10)

    if sort == "price_asc":
        query = query.order_by(TravelProgram.price_per_person.asc())
    elif sort == "price_desc":
        query = query.order_by(TravelProgram.price_per_person.desc())
    elif sort == "duration":
        query = query.order_by(TravelProgram.duration_days.asc())
    else:
        query = query.order_by(TravelProgram.is_featured.desc(), TravelProgram.view_count.desc())

    pagination = query.paginate(page=page, per_page=9, error_out=False)
    themes = db.session.query(TravelProgram.theme).filter(TravelProgram.theme.isnot(None)).distinct().all()

    return render_template(
        "programs/list.html",
        programs=pagination.items,
        pagination=pagination,
        themes=[t[0] for t in themes],
        current_theme=theme,
        current_duration=duration,
        current_sort=sort,
    )


@bp.route("/<slug>")
def detail(slug):
    program = TravelProgram.query.filter_by(slug=slug, is_active=True).first_or_404()
    program.view_count = (program.view_count or 0) + 1
    db.session.commit()

    days = list(program.days.order_by("day_number").all())
    testimonials = []
    related = TravelProgram.query.filter(
        TravelProgram.theme == program.theme,
        TravelProgram.id != program.id,
        TravelProgram.is_active == True,
    ).limit(3).all()

    return render_template(
        "programs/detail.html",
        program=program,
        days=days,
        testimonials=testimonials,
        related=related,
    )
