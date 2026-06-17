from flask import render_template, redirect, url_for, flash, request
from . import bp, admin_required, super_admin_required
from ...extensions import db
from ...models.hotel import Hotel
from ...models.destination import Destination
from ...forms.admin_forms import HotelForm
from slugify import slugify


@bp.route("/hotels")
@admin_required
def hotel_list():
    page = request.args.get("page", 1, type=int)
    hotels = Hotel.query.order_by(Hotel.name).paginate(page=page, per_page=20)
    return render_template("admin/hotels/list.html", hotels=hotels.items, pagination=hotels)


@bp.route("/hotels/nouveau", methods=["GET", "POST"])
@admin_required
def hotel_create():
    form = HotelForm()
    form.destination_id.choices = [(d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()]
    if form.validate_on_submit():
        hotel = Hotel()
        _fill_hotel(hotel, form)
        db.session.add(hotel)
        db.session.commit()
        flash("Hôtel créé.", "success")
        return redirect(url_for("admin.hotel_list"))
    return render_template("admin/hotels/form.html", form=form, title="Nouvel hôtel")


@bp.route("/hotels/<int:hotel_id>/modifier", methods=["GET", "POST"])
@admin_required
def hotel_edit(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    form = HotelForm(obj=hotel)
    form.destination_id.choices = [(d.id, d.name_fr) for d in Destination.query.order_by(Destination.name_fr).all()]
    if form.validate_on_submit():
        _fill_hotel(hotel, form)
        db.session.commit()
        flash("Hôtel mis à jour.", "success")
        return redirect(url_for("admin.hotel_list"))
    return render_template("admin/hotels/form.html", form=form, hotel=hotel, title="Modifier l'hôtel")


@bp.route("/hotels/<int:hotel_id>/supprimer", methods=["POST"])
@super_admin_required
def hotel_delete(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash("Hôtel supprimé.", "success")
    return redirect(url_for("admin.hotel_list"))


def _fill_hotel(hotel, form):
    hotel.name = form.name.data
    hotel.slug = form.slug.data or slugify(form.name.data)
    hotel.destination_id = form.destination_id.data
    hotel.hotel_type = form.hotel_type.data
    hotel.stars = form.stars.data
    hotel.address = form.address.data
    hotel.latitude = form.latitude.data
    hotel.longitude = form.longitude.data
    hotel.description_fr = form.description_fr.data
    hotel.price_min = form.price_min.data
    hotel.price_max = form.price_max.data
    hotel.has_pool = form.has_pool.data
    hotel.has_spa = form.has_spa.data
    hotel.has_restaurant = form.has_restaurant.data
    hotel.has_wifi = form.has_wifi.data
    hotel.booking_url = form.booking_url.data
    hotel.is_partner = form.is_partner.data
    hotel.is_featured = form.is_featured.data
    hotel.is_active = form.is_active.data
