from flask import Blueprint, render_template
from ..models.airline import Airline, FlightPromotion

bp = Blueprint("airlines", __name__)


@bp.route("/")
def list_airlines():
    airlines = Airline.query.filter_by(is_active=True).all()
    promos = FlightPromotion.query.filter_by(is_active=True).order_by(FlightPromotion.created_at.desc()).limit(8).all()
    return render_template("airlines/list.html", airlines=airlines, promos=promos)


@bp.route("/<slug>")
def detail(slug):
    airline = Airline.query.filter_by(slug=slug, is_active=True).first_or_404()
    promos = airline.promotions.filter_by(is_active=True).all()
    return render_template("airlines/detail.html", airline=airline, promos=promos)
