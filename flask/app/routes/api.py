from flask import Blueprint, jsonify, request
from ..models.destination import Destination
from ..models.program import TravelProgram
from ..models.hotel import Hotel

bp = Blueprint("api", __name__)


@bp.route("/destinations")
def api_destinations():
    query = Destination.query.filter_by(is_active=True)
    search = request.args.get("q", "")
    if search:
        query = query.filter(
            (Destination.name_fr.ilike(f"%{search}%")) | (Destination.name_en.ilike(f"%{search}%"))
        )
    destinations = query.limit(20).all()
    return jsonify([
        {
            "id": d.id,
            "slug": d.slug,
            "name_fr": d.name_fr,
            "name_en": d.name_en,
            "country": d.country.name_fr if d.country else "",
            "latitude": float(d.latitude) if d.latitude else None,
            "longitude": float(d.longitude) if d.longitude else None,
            "image": d.image_main,
            "type": d.destination_type,
        }
        for d in destinations
    ])


@bp.route("/destinations/<int:dest_id>/map")
def destination_map_data(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    hotels = Hotel.query.filter_by(destination_id=dest_id, is_active=True).all()
    return jsonify({
        "destination": {
            "lat": float(dest.latitude) if dest.latitude else None,
            "lng": float(dest.longitude) if dest.longitude else None,
            "name": dest.name_fr,
            "street_view_lat": float(dest.street_view_lat) if dest.street_view_lat else None,
            "street_view_lng": float(dest.street_view_lng) if dest.street_view_lng else None,
        },
        "hotels": [
            {
                "id": h.id,
                "name": h.name,
                "lat": float(h.latitude) if h.latitude else None,
                "lng": float(h.longitude) if h.longitude else None,
                "stars": h.stars,
                "price_min": float(h.price_min) if h.price_min else None,
            }
            for h in hotels
        ],
    })


@bp.route("/search")
def global_search():
    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify({"destinations": [], "programs": [], "hotels": []})

    destinations = Destination.query.filter(
        Destination.is_active == True,
        (Destination.name_fr.ilike(f"%{q}%")) | (Destination.name_en.ilike(f"%{q}%"))
    ).limit(5).all()

    programs = TravelProgram.query.filter(
        TravelProgram.is_active == True,
        (TravelProgram.name_fr.ilike(f"%{q}%")) | (TravelProgram.name_en.ilike(f"%{q}%"))
    ).limit(5).all()

    return jsonify({
        "destinations": [{"id": d.id, "name": d.name_fr, "slug": d.slug, "image": d.image_main} for d in destinations],
        "programs": [{"id": p.id, "name": p.name_fr, "slug": p.slug, "days": p.duration_days} for p in programs],
    })
