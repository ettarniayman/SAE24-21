from flask import Blueprint, render_template, request
from ..models.hotel import Hotel
from ..models.destination import Destination

bp = Blueprint("hotels", __name__)


@bp.route("/")
def list_hotels():
    page = request.args.get("page", 1, type=int)
    dest_id = request.args.get("dest", type=int)
    hotel_type = request.args.get("type", "")
    stars = request.args.get("stars", type=int)

    query = Hotel.query.filter_by(is_active=True)
    if dest_id:
        query = query.filter_by(destination_id=dest_id)
    if hotel_type:
        query = query.filter_by(hotel_type=hotel_type)
    if stars:
        query = query.filter_by(stars=stars)

    query = query.order_by(Hotel.is_featured.desc(), Hotel.rating.desc())
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    destinations = Destination.query.filter_by(is_active=True).order_by(Destination.name_fr).all()

    return render_template(
        "hotels/list.html",
        hotels=pagination.items,
        pagination=pagination,
        destinations=destinations,
        current_dest=dest_id,
        current_type=hotel_type,
        current_stars=stars,
    )


@bp.route("/<slug>")
def detail(slug):
    hotel = Hotel.query.filter_by(slug=slug, is_active=True).first_or_404()
    medias = list(hotel.medias.filter_by(is_active=True).all())
    related = Hotel.query.filter(
        Hotel.destination_id == hotel.destination_id,
        Hotel.id != hotel.id,
        Hotel.is_active == True,
    ).limit(3).all()
    return render_template("hotels/detail.html", hotel=hotel, medias=medias, related=related)
